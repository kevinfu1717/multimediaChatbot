import paddlehub as hub

love_module = hub.Module(name="ernie_gen_lover_words")
if __name__=='__main__':
    test_texts = ['情人节', '故乡', '小编带大家了解一下程序员情人节']
    results = love_module.generate(texts=test_texts, beam_width=1)
    for result in results:
        print(result)