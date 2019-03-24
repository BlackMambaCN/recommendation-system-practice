from gensim.models.ldamodel import LdaModel
from gensim.corpora.dictionary import Dictionary
import sys 
import argparse

class LDA(object):
    def __init__(self, topics=10,
                worker=3,
                pretrained_model=None,
                dictionary=None):
        """ lda模型训练初始化
        Args:
            topics -- 指定主题个数
            worker -- 并行化参数，一般为core数量减一
            pretrained_model -- 预训练模型，由于支持在线更新，所以可以加载上次训练的模型
            dictionary -- 训练时词需要转换成ID，所以跟模型配套有一个ID映射的字典
        Example:
            >>> lda = LDA(topics = 20, worker = 2, 
                          pretrained_model = model_file, 
                          dictionary = dictionary_file)
            >>> corpus = read_file(corpus_file) # [['word1', 'word2'], ['word3', 'word4']]
            >>> lda.update(corpus)
            >>> lda.save(model_file, dictionary_file)
            >>> topics = lda.inference(['word5', 'word6'])
        """
        
        self._topics = topics
        self._workers = worker
        self._model = None
        self._common_dictionary = None
        
        if pretrained_model and dictionary:
            self._model = LdaModel.load(pretrained_model) # 加载预训练模型
            self._common_dictionary = Dictionary.load(dictionary) # 载入字典
        
    def save(self, model_file, dictionary_file):
        """
        保存训练的模型，同时保存对应的字典
        Args:
            model_file - 模型文件
            dictionary_file - 词典文件
        Returns:
            None
        """
        if self._model:
            self._model.save(model_file)
        if self._common_dictionary:
            self._common_dictionary.save(dictionary_file)
        
    def update(self, corpus = [[]]):
        """
        在线更新，在已有模型的基础上在线更新
        Args:
            corpus - 用于更新的文档列表
        """
        if not self._model and len(corpus) > 0:
            # 创建字典，每一个词都给予一个索引
            self._common_dictionary = Dictionary(corpus)
            corpus_data = [self._common_dictionary.doc2bow(sentence) for sentence in corpus]
            # corpus_data 词袋矩阵 topics 主题数 id2word 将索引转化为词 passes 训练轮数
            self._model = LdaModel(corpus_data, self._topics, id2word=self._common_dictionary, passes=50)
            #self._model = LdaModel(corpus_data, self._topics)
        elif self._model and len(corpus) > 0:
            self._common_dictionary.add_documents(corpus)
            new_corpus_data = [self._common_dictionary.doc2bow(sentence) for sentence in corpus]
            self._model.update(new_corpus_data)
    
    def inference(self, document = []):
        """
        新文档推断话题分布
        Args:
            document - 文档，词列表
        Returns:
            话题分布列表
        """
        if self._model:
            doc = [self._common_dictionary.doc2bow(document)]
            return self._model.get_document_topics(doc)
        return []
        
    @property
    def model(self):
        return self._model
        
    @property
    def dictionary(self):
        return self._common_dictionary
    
if __name__ == '__main__':
    # argparse命令行解析，获取命令行参数
    # -m 预训练模型地址 -c 预料库文件 -s 训练模型保存地址 -d 字典保存地址 -t 主题数
    parser = argparse.ArgumentParser(description = '训练词向量及查询词相似性')
    parser.add_argument('-m', '--model', type = str, default = None, help = """ pretrained model """)
    parser.add_argument('-c', '--corpus', help = """ corpus file """)
    parser.add_argument('-s', '--save', help = """ save new model """)
    parser.add_argument('-d', '--dictionary', type = str, default = None, help = """ dictionary """)
    parser.add_argument('-t', '--topics', type = int, default = 10, help = """ number of topics """)
    args = vars(parser.parse_args())
    
    lda = LDA(topics = args['topics'],
             pretrained_model = args['model'],
             dictionary = args['dictionary'])
    
    sentences = []
    with open(args['corpus'], 'r') as corpus_file:
        for line in corpus_file:
            words = line.strip().split()
            if len(words) == 0:
                continue
            sentences.append(words)

    lda.update(sentences)
    lda.save(args['save'], args['dictionary']) # 保存训练模型，保存语料库字典
    
    # 打印前num_topics个topic的前num_words个词的词分布
    topics = lda.model.print_topics(num_topics = 2, num_words = 3)
    
    print('print topics: \n', topics)
    #[(1, '0.018*"at" + 0.018*"do" + 0.018*"I"'), (8, '0.054*"driving" + 0.054*"sister" + 0.054*"father"')]
    for topic in topics:
        words = []
        for word_value in topic[1].split('+'):
            value, word = word_value.split('*')
            word = word.strip()
            #word = lda.dictionary[int(word[1:-1])]
            words.append("%s:%s" % (word, value))
        print(" ".join(words))
    
    ''' 对新文档主题进行预测 '''
    while 1:
        print('输入一段话: ')
        line = sys.stdin.readline()
        line = line.strip()
        if line == 'exit' or line == 'quit' or line == 'q':
            break
           
        words = line.split()
        topics = lda.inference(words)
        print('新文档的主题分布为: ')
        for topic in topics:
            print(topic)
        
    
            