import paddlehub as hub
import numpy as np
couplet_module = hub.Module(name="ernie_gen_couplet")
if __name__=='__main__':
    test_texts = ["特朗普只会针对中国，太可恶了，扁他",'头大无脑，只会吹嘘','专做损人不利己的事请']
    nums=5
    test_texts=['绣花枕头，不会跳舞不会唱歌']
    results = couplet_module.generate(texts=test_texts,  beam_width=nums)
    for result in results:
        print(result[np.random.randint(nums)])