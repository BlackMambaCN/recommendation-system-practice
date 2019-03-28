package test;

import org.ansj.domain.Result;
import org.ansj.domain.Term;
import org.ansj.splitWord.analysis.ToAnalysis;

import java.io.IOException;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class AnsjTest {

    public static void main(String[] args) throws IOException {
        test();
    }

    public static void test() {
        // 关注某些词性的词
        Set<String> expectedNature = new HashSet<String>() {{
            add("n");add("v");add("vd");add("vn");add("vf");
            add("vx");add("vi");add("vl");add("vg");
            add("nt");add("nz");add("nw");add("nl");
            add("ng");add("userDefine");add("wh");
        }};
        String str = "欢迎使用ansj_seg,(ansj中文分词)在这里如果你遇到什么问题都可以联系我.我一定尽我所能.帮助大家.ansj_seg更快,更准,更自由!";
        Result result = ToAnalysis.parse(str); // 分词结果的一个封装，List<Term>

        System.out.println(result.getTerms()); // [欢迎/v, 使用/v, ansj/en, _, seg/en,

        List<Term> terms = result.getTerms(); // terms
        System.out.println(terms.size()); // 43

        for (int i = 0; i < terms.size(); i++) {
            String word = terms.get(i).getName(); // 词
            String natureStr = terms.get(i).getNatureStr(); // 词性
            if (expectedNature.contains(natureStr)) {
                System.out.println(word + ":" + natureStr);
            }
        }
    }
}
