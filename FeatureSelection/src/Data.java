import java.io.BufferedReader;
import java.io.FileReader;
import java.util.Arrays;

/**
 * @author nerrtica
 * @since 2015/01/27
 */
public class Data {
	public static double[][] feature;
	public static int[] label;
	public static int featureNum, dataNum, intervalNum;
	public static String featureFileRoute, labelFileRoute;
	public static boolean isDiscrete;
	public static int[] bestFeature;
	
	public static int NEIGHBOR_NUM = 7;
	
	//set best feature in numeral order
	public static void setBestFeature () {
		bestFeature = new int[featureNum];
		for (int i = 0; i < featureNum; i++) {
			bestFeature[i] = i;
		}
	}
	
	//set best feature cloning featureList parameter
	public static void setBestFeature (int[] featureList) {
		bestFeature = new int[featureNum];
		bestFeature = featureList.clone();
	}
	
	//read feature data file
	public static void readFeature (String featureRoute, boolean isDiscrete) throws Exception {
		BufferedReader bfreader = new BufferedReader(new FileReader(featureRoute));
		int index = 0;
		
		while (true) {
			String temp = bfreader.readLine();
			if (temp == null) {
				dataNum = index;
				bfreader.close();
				break;
			}
			index++;
		}
		
		index = 0;
		bfreader = new BufferedReader(new FileReader(featureRoute));
		featureFileRoute = featureRoute;
		Data.isDiscrete = isDiscrete;
		bfreader.readLine();
		while (true) {
			String temp = bfreader.readLine();
			if (temp == null) {
				break;
			}
			if (index == 0) {
				String[] data = temp.split(",");
				featureNum = data.length - 1;
				feature = new double[dataNum][featureNum];
				//continue;
			}
			splitFeature(temp, index++);
		}
		bfreader.close();
	}
	
	private static void splitFeature (String line, int index) {
		String[] data = line.split(",");
		for (int i = 0; i < featureNum; i++) {
			feature[index][i] = Double.parseDouble(data[i + 1]);
		}
	}
	
	//read feature data file
	public static void readLabel (String labelRoute) throws Exception {
		BufferedReader bfreader = new BufferedReader(new FileReader(labelRoute));
		int index = 0;
		
		labelFileRoute = labelRoute;
		while (true) {
			String temp = bfreader.readLine();
			if (temp == null) { break; }
			if (index == 0) {
				label = new int[dataNum];
			}
			label[index++] = Integer.parseInt(temp);
		}
		bfreader.close();
	}
	
	public static void setInterval (int featureIndex) {
		if (!isDiscrete) {
			intervalNum = 3;
			return;
		}
		
		double[] featureTemp = new double[dataNum];
		for (int i = 0; i < dataNum; i++) {
			featureTemp[i] = feature[i][featureIndex];
		}
		Arrays.sort(featureTemp);
		
		int index = 0;
		double previous = featureTemp[0];
		for (int i = 0; i < dataNum; i++) {
			if (featureTemp[i] != previous) {
				index++;
			}
		}
		intervalNum = index + 1;
	}
	
	public static void setNeighborNum (int neighborNum) {
		NEIGHBOR_NUM = neighborNum;
	}
}
