import java.io.BufferedReader;
import java.io.FileReader;


public class Main {

	final static double minChi = 4;
	static String[] featureList;
	
	public static void main(String[] args) {
		try {
			Data.readFeature(args[0], false);
			Data.readLabel(args[1]);
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		ChiSquare.play(4);
		
		try {
			BufferedReader bfreader = new BufferedReader(new FileReader("./FeatureList.csv"));
			String temp = bfreader.readLine();
			featureList = temp.split(",");
			bfreader.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		for (int i = 0; i < Data.featureNum; i++) {
			System.out.printf("%d : %s\n", i + 1, featureList[Data.bestFeature[i]]);
		}
	}
}
