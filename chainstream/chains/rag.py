def answer(question: str, llm, vectorstore, template=None, prompt=None):
    from transformers.pipelines.text_generation import TextGenerationPipeline
    from chainstream.utils.documents import format_docs

    if isinstance(llm, TextGenerationPipeline):
        context = format_docs(vectorstore.similarity_search(question))
        prompt = [
            {
                "role": "user",
                "content": f"""Use the following pieces of context to answer the question at the end.
                If you don't know the answer, just say that you don't know, don't try to make up an answer.
                Use three sentences maximum and keep the answer as concise as possible.
                Always say "thanks for asking!" at the end of the answer.
                
                {context}
                
                Question: {question}
                
                Helpful Answer:""",
            }
        ]
        generation_args = {
            "max_new_tokens": 500,
            "return_full_text": False,
            "temperature": 0.0,
            "do_sample": False,
        }
        response = llm(prompt, **generation_args)[0]["generated_text"]
        return {
            "context": context,
            "question": question,
            "answer": response.strip(),
        }
    else:
        from langchain_core.prompts import PromptTemplate
        from langchain_core.runnables import RunnablePassthrough, RunnableParallel
        from langchain_core.output_parsers import StrOutputParser

        if template is None and prompt is None:
            template = """Use the following pieces of context to answer the question at the end.
            If you don't know the answer, just say that you don't know, don't try to make up an answer.
            Use three sentences maximum and keep the answer as concise as possible.
            Always say "thanks for asking!" at the end of the answer.

            {context}

            Question: {question}

            Helpful Answer:"""
        if prompt is None:
            prompt = PromptTemplate.from_template(template)

        chain = RunnableParallel(
            {
                "context": vectorstore.as_retriever(),
                "question": RunnablePassthrough(),
            }
        ).assign(
            answer=(
                RunnablePassthrough.assign(
                    context=(lambda x: format_docs(x["context"]))
                )
                | prompt
                | llm
                | StrOutputParser()
            )
        )
        return chain.invoke(question)
