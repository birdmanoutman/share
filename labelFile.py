import docx
from torch.nn.functional import softmax
from transformers import BertTokenizer, BertForSequenceClassification

# 加载预训练模型和分词器，换成中文的模型
model_name = 'bert-base-chinese'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_lables=5)


def classify_text(text):
    inputs = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors="pt")
    outputs = model(**inputs)
    probs = softmax(outputs.logits, dim=-1)
    label_index = probs.argmax().item()  # 获取最高概率的标签索引

    # 假设你的模型有两个标签：0表示"负面"，1表示"正面"
    chinese_labels = ["汽车", "财经", "体育", "文化", "汽车设计"]  # 这里需要根据你的模型实际情况进行调整
    return chinese_labels[label_index]  # 返回中文标签


def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = [paragraph.text for paragraph in doc.paragraphs]
    return "\n".join(text)


# 示例：对一个Word文档进行处理
docx_text = extract_text_from_docx("./TXT/1225 附件三：研发总院2023年度优秀团队奖申请表.docx")
label = classify_text(docx_text)
print("The label for the document is:", label)
