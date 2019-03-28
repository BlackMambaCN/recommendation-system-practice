package test;

import java.util.HashSet;
import java.util.Set;

public class AnsjTest {
    public static void test() {
        // 关注某些词性的词
        Set<String> expectedNature = new HashSet<String>() {{
            add("n");add("v");add("vd");add("vn");add("vf");
            add("vx");add("vi");add("vl");add("vg");
            add("nt");add("nz");add("nw");add("nl");
            add("ng");add("userDefine");add("wh");
        }};
        //String str = ""
    }
}
