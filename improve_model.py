from transformers import Trainer, TrainingArguments, AutoModelForSequenceClassification, AutoTokenizer
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
from torch.nn import CrossEntropyLoss
from pull_from_postgresql import * 
from add_to_postgresql import * 
from datasets import Dataset
import torch
tokenizer = AutoTokenizer.from_pretrained("Qualcomm-AI-Research/BamiBERT")

list_label = [
	{"label":"fail"},
	{"label":"success"},
]
id2label_label = {i:label['label'] for i, label in enumerate(list_label)}
label2id_label = {label['label']:i for i, label in enumerate(list_label)}

lang = 'en'
with open("path_to_last_trained_model.txt","r") as f:
    path_to_latest_model = f.read()

outcome_classifier = AutoModelForSequenceClassification.from_pretrained(
    path_to_latest_model,
    num_labels=2,
    id2label=id2label_label,
    label2id=label2id_label,
)

def compute_metrics(pred):
    global num_labels
    num_labels = 2
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='macro')
    acc = accuracy_score(labels, preds)
    loss_fct = CrossEntropyLoss()
    logits = torch.tensor(pred.predictions)
    labels = torch.tensor(labels)
    loss = loss_fct(logits.view(-1, num_labels), labels.view(-1))
    return {
        'accuracy@'+lang: acc,
        'f1@'+lang: f1,
        'precision@'+lang: precision,
        'recall@'+lang: recall,
        'loss@'+lang: loss,
    }

training_args = TrainingArguments(
    eval_strategy="epoch",
    logging_strategy="epoch",
    learning_rate=1e-5,
    num_train_epochs=2,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    output_dir="./models/formal_informal_classification/new_model",
    remove_unused_columns=False,
    save_total_limit=1,
    optim="adamw_torch",

    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    greater_is_better=False,



    logging_steps=1,          # print loss mỗi 1 step (để debug/xem cụ thể)
    logging_first_step=True,
)

def train(train_dataset,valid_dataset):
    trainer = Trainer(
        model=outcome_classifier,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=valid_dataset,
        compute_metrics=compute_metrics
    )
    train_result = trainer.train(resume_from_checkpoint = False)

    with open("path_to_last_trained_model.txt","w") as f:
        f.write(str(trainer.state.best_model_checkpoint))

    return trainer.state.best_model_checkpoint


def improve_model(new_conversations): 
    print("----------start training--------------")
    random_old_conversations = choose_random_from_database(20)
    new_conversations_list = []
    print(new_conversations)
    random_old_conversations_list_dict = []
    for c in random_old_conversations: 
        random_old_conversations_list_dict.append({"text":c[0],"label":c[1]})
    for conversation in new_conversations:
        if conversation["label"] == "success":
            for sentence in conversation["conversation"] :
                if sentence["speaker"] == "client" :
                    sentence.pop('speaker', None)
                    new_conversations_list.append(sentence)

    add_to_database(new_conversations_list)
    
    dataset = random_old_conversations_list_dict + new_conversations_list
    dataset = Dataset.from_list(dataset)

    dataset = dataset.train_test_split(test_size=0.2, seed=42)
    train_dataset = dataset["train"]
    valid_dataset = dataset["test"]

    

    train_dataset = train_dataset.map(tokenize_fn, batched=True)
    valid_dataset = valid_dataset.map(tokenize_fn, batched=True)

    train(train_dataset,valid_dataset)


    print("----------end training--------------")

def tokenize_fn(batch):
    return tokenizer(batch["text"], truncation=True, padding="max_length", max_length=128)


# trainer.evaluate(metric_key_prefix='test_en',
#                 eval_dataset=eval_dataset)

# new_c =[{'conversation': [{'speaker': 'client', 'text': 'Hello bạn ', 'label': 1}, {'speaker': 'salebot', 'text': 'Chào bạn! 😄 2 chữ thôi mà nghe ngọt ghê. Bạn cần tư vấn guitar hả? Nói thiệt đi, mình loại nào cũng có nè—đàn mới, đàn cũ, acoustic hay electric, giá sinh viên luôn. Bạn thích dòng nào, để mình khoe hàng liền! 🎸'}, {'speaker': 'client', 'text': 'giá sinh viên thôi ', 'label': 0}, {'speaker': 'salebot', 'text': 'Dạ, em hiểu rồi ạ. Với mức "giá sinh viên" thì em xin phép tư vấn mấy dòng acoustic tầm trung, giá mềm mà chất lượng ổn định cho bạn mới tập:\n\n- **Fender CD-60S** (khoảng 3.5 - 4 triệu): âm ấm, dễ bấm, thương hiệu uy tín.\n- **Yamaha F310** (khoảng 2.8 - 3.2 triệu): bền bỉ, tiếng rõ, hợp túi tiền.\n- **Cort AD810** (khoảng 2.5 - 3 triệu): giá rẻ nhất mà vẫn chơi tốt, phù hợp sinh viên.\n\nNếu bạn cần phụ kiện (capo, dây đàn, bao đàn) em gói combo luôn, giảm thêm 5% nữa ạ. Anh/chị muốn xem chi tiết model nào, em gửi thông số và hình thực tế qua đây nhé?'}, {'speaker': 'client', 'text': 'thôi đắt quá nghỉ đi cảm ơn nhé ', 'label': 1}, {'speaker': 'salebot', 'text': 'Dạ không sao đâu bạn hiền! 😄 Mình hiểu mà, giá đó với sinh viên cũng hơi căng thật. Nhưng khoan vội nghỉ nha—để mình gợi ý thêm mấy em **giá "hạt dẻ" hơn nữa**, tầm 1.5 - 2 triệu thôi, vẫn chơi ngon lành cho người mới tập:\n\n- **Kawasaki K-15** (tầm 1.8tr): tiếng khá, phím êm, hợp túi tiền.\n- **Vang VS-1** (tầm 1.5tr): rẻ nhất mà vẫn đánh được, dân sinh viên hay chọn.\n- Hoặc nếu bạn muốn để dành thêm ít bữa, mình giữ hàng cho tới cuối tháng, có gì ghé lại chơi thử cũng được.\n\nCòn nếu bạn vẫn thấy chưa ưng, thì thôi mình cũng cảm ơn bạn đã ghé. Khi nào có nhu cầu hoặc muốn hỏi thêm gì về đàn, cứ nhắn mình, mình hỗ trợ nhiệt tình liền! Chúc bạn vui nha! 🎸'}, {'speaker': 'client', 'text': 'ừ cảm ơn nhé mà cũng không muốn mua đâu ', 'label': 1}], 'label': 'fail'}, {'conversation': [{'speaker': 'client', 'text': 'Xin chào bạn ', 'label': 0}, {'speaker': 'salebot', 'text': 'Xin chào quý khách!  \nTôi rất hân hạnh được phục vụ. Quý khách cần tư vấn về dòng guitar nào ạ? (Acoustic, classic hay electric?)'}, {'speaker': 'client', 'text': 'classic đi ', 'label': 1}, {'speaker': 'salebot', 'text': 'Chuẩn luôn! Classic nghe là mê rồi đó.  \nBạn thích dòng nào hơn: **đàn classic truyền thống** (tiếng ấm, dây nylon) hay **classic điện** (gắn cảm biến, chơi sân khấu)?  \nĐể mình gợi ý mấy em ngon – bình dân mà chất, hợp túi tiền sinh viên nè! 😎'}, {'speaker': 'client', 'text': 'nylon tầm 1 tr đổ xuống ', 'label': 1}, {'speaker': 'salebot', 'text': 'Ok nghe! Nylon tầm 1 triệu đổ xuống thì mình có mấy em ngon lành cành đào nè.  \n\n- **Yamaha C40** – huyền thoại cho người mới, tiếng ấm, bền bỉ, giá tầm 1tr2 (hơi quá xíu nhưng đáng đồng tiền).  \n- **Kawaii Classic 100** – tầm 900k, tiếng trong, phím êm, hợp học đệm hát.  \n- **Fender CN-140** – tầm 1tr, thùng nhỏ gọn, dễ bấm, màu đẹp.  \n\nBạn muốn mình check thêm màu nào, hay cần tư vấn phụ kiện (capo, dây, bao đàn) luôn không? 😄'}, {'speaker': 'client', 'text': 'Thế kawaii nhé mình ok đó mà sợ chất lượng hơi kém ', 'label': 1}, {'speaker': 'salebot', 'text': 'Dạ em hiểu mà! Sợ chất lượng kém là đúng tâm lý, nhất là hàng tầm giá đó.  \n\nNhưng anh/chị yên tâm nha:  \n- **Kawaii Classic 100** là dòng bán chạy nhất shop, mình nhập trực tiếp từ hãng, có **hóa đơn VAT** và **giấy chứng nhận nguồn gốc** rõ ràng.  \n- Shop em hoạt động **5 năm**, điểm đánh giá **4.9/5** từ hơn 1000 khách – anh/chị có thể xem review thật trên page.  \n- Đặc biệt, em cho **kiểm tra hàng trước khi thanh toán** (COD). Nếu không ưng, anh/chị trả lại, em chịu phí ship luôn.  \n\nMà nếu anh/chị vẫn phân vân, em gửi thêm **video demo tiếng đàn** và **ảnh thực tế** từ kho để anh/chị xem trước nha. Chất lượng mà không đạt, em bồi thường gấp đôi tiền cọc luôn! 😉'}, {'speaker': 'client', 'text': 'thế cod đi địa chỉ 123 đường abc ở hà nội nhé sđt 0123456789', 'label': 0}, {'speaker': 'salebot', 'text': 'Dạ, em xin ghi nhận thông tin đặt hàng của quý khách như sau:\n\n- **Sản phẩm:** Đàn guitar classic Kawaii Classic 100 (dây nylon)  \n- **Giá:** 900.000 VNĐ (đã bao gồm phí giao hàng nội thành Hà Nội)  \n- **Hình thức thanh toán:** COD – quý khách kiểm tra hàng trước khi thanh toán  \n- **Địa chỉ giao:** 123 đường ABC, Hà Nội  \n- **Số điện thoại:** 0123456789  \n\nEm xin xác nhận lại: Quý khách có cần thêm phụ kiện kèm theo (capo, dây đàn dự phòng, bao đàn) không ạ? Nếu không, em sẽ tiến hành đóng gói và giao hàng trong vòng **24 giờ** tới.  \n\nEm sẽ gọi điện xác nhận trước khi giao để chắc chắn quý khách có nhà. Cảm ơn quý khách đã tin tưởng shop! 🙏'}], 'label': 'success'}, {'conversation': [{'speaker': 'client', 'text': 'alo ở đây có đàn gì nhể ', 'label': 1}, {'speaker': 'salebot', 'text': 'Ê, ở đây đủ loại đàn luôn nha mày! Có acoustic, classic, electric, bass, rồi cả ukulele nữa. Mày thích loại nào, chơi thể loại gì, để tao tư vấn cho chuẩn nè!'}, {'speaker': 'client', 'text': 'ê cứng nhỉ, cho bass đê sắp biểu diễn rồi ', 'label': 1}, {'speaker': 'salebot', 'text': 'Chuẩn luôn! Bass đây, nghe là biết chơi máu liền. Mày cần bass 4 dây hay 5 dây? Active hay passive? Tao có mấy em bass giá ngon, chơi live cực đã, bass thùng to, tiếng chắc nịch luôn. Sắp diễn thì phải chọn cây nào "chất" để còn quẩy tới bến chứ! Vô đây thử liền đi, tao để dành cho mày đó!'}, {'speaker': 'client', 'text': 'haha đc 4 dây loại ngon nhất đi cho đã ', 'label': 1}, {'speaker': 'salebot', 'text': 'Ê ngon! 4 dây mà "ngon nhất" thì để tao khoe em này: **Ibanez GSR200** hoặc **Squier Affinity Jazz Bass** — chơi live là khỏi chê, tiếng bass nặng trịch, sâu lắng mà vẫn rõ từng nốt. Mày thích màu gì? Đen huyền bí hay đỏ cháy? Tao ship tận nơi, còn tặng dây đàn + túi đệm luôn. Giá để tao nói nhỏ: chỉ tầm 5-6 củ, bảo hành 12 tháng, chơi thử 7 ngày không ưng trả lại! Quất luôn không mày? 😎'}, {'speaker': 'client', 'text': 'chốt luôn ibanez gsr200 t tới tận quán mua cũng tiện đường tới ', 'label': 1}, {'speaker': 'salebot', 'text': 'Ok chốt! Ibanez GSR200 màu đen huyền thoại, tao để dành riêng cho mày đó. Tới quán cứ gọi thẳng tên tao, tao đem ra cho mày test thử liền — tiếng bass nó "bụp" phát là mê ngay. Nhớ mang theo amp hoặc headphone nếu muốn nghe thử cho đã, chứ quán tao loa bass cũng khá phê. Địa chỉ: 123 Nguyễn Trãi, Q.1, ngay ngã tư dễ tìm. Tới nói "anh ơi em chốt con GSR200" là tao biết liền! Đi đường cẩn thận, tao chờ nha! 🎸🔥'}, {'speaker': 'client', 'text': 'ok cảm ơn hehe ', 'label': 1}, {'speaker': 'salebot', 'text': 'Ê khỏi cảm ơn! Tao lo cho mày hết, tới đây tao pha cà phê sẵn, test đàn xong chốt giá là mày ưng bụng liền. Đi đường nhớ đeo khẩu trang, trời nắng ghê. Gặp nha! 🤙😄'}], 'label': 'success'}]
# improve_model(new_c)