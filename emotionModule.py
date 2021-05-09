import paddlehub as hub

emotion_module = hub.Module(name="emotion_detection_textcnn")
if __name__=='__main__':
    test_text = ["今天天气真好"]
    results = emotion_module.emotion_classify(texts=test_text)

    for result in results:
        print(result['text'])
        print(result['emotion_label'])
        print(result['emotion_key'])
        print(result['positive_probs'])
        print(result['negative_probs'])
        print(result['neutral_probs'])