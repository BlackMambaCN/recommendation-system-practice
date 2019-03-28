package test;
import com.ansj.vec.Learn;
import com.sun.xml.internal.xsom.impl.Ref;

import java.io.*;
import java.util.List;

import org.ansj.domain.Result;
import org.ansj.domain.Term;
import org.ansj.splitWord.analysis.ToAnalysis;

import com.alibaba.fastjson.JSONObject;
import org.nlpcn.commons.lang.util.StringUtil;

public class Word2VecTest {
    public static String corpusPath;

    private static final File corpusFile = new File("./src/main/resources/corpus/swresult_withoutnature.txt");

    public static void main(String[] args) throws IOException {

        //File file2 = new File("./src/main/resources/corpus").getAbsoluteFile();
        //System.out.println(file2);

        File[] files = new File("./src/main/resources/corpus/").listFiles();

        System.out.println(files[0].getName());

        // 构建语料
        /*
        try (FileOutputStream fos = new FileOutputStream(corpusFile)) {
            for (File file : files) {
                if (file.canRead() && file.getName().endsWith(".txt")) {
                    System.out.println(file.getName());
                    parserFile(fos, file);
                }
            }
        }*/
        //

        // 进行分词训练
        Learn learn = new Learn();
        learn.learnFile(corpusFile);
        learn.saveModel(new File("./src/main/resources/models/vector.md"));

        // 加载测试

    }

    private static void parserFile(FileOutputStream fos, File file) throws FileNotFoundException, IOException {
        FileReader fr = new FileReader("");
        try (BufferedReader br = new BufferedReader(fr)){
            String temp = null;
            JSONObject parse = null;
            while ((temp = br.readLine()) != null) {
                parse = JSONObject.parseObject(temp);
                parserStr(fos, parse.getString("title"));
                parserStr(fos ,StringUtil.rmHtmlTag(parse.getString("content")));
            }
        }
    }

    // 对title进行分词，并保存到fos文件中
    private static void parserStr(FileOutputStream fos, String title) throws IOException {
        Result parse2 = ToAnalysis.parse(title);
        //System.out.println(parse2.toString());
        StringBuilder sb = new StringBuilder();
        for (Term term : parse2) {
            sb.append(term.getName());
            sb.append(" ");
        }
        fos.write(sb.toString().getBytes());
        fos.write("\n".getBytes());
    }
}
