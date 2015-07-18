import java.util.ArrayList;
import java.util.Arrays;

/**
 * @author nerrtica
 * @since 2015/01/29
 */
public class ChiSquare {
	private static double[][] chiSquare;
	private static int[][] chiTable;
	private static int[] labelIndex;
	private static double max, min;
	private static int[] bestFeature;
	private static int labelCount = 10;
	public static ArrayList<String> result = new ArrayList<String>();
	
	public static int play (double minChi) {
		chiSquare = new double[Data.featureNum][2];
		labelIndex = new int[Data.dataNum];
		bestFeature = new int[Data.featureNum];
		for (int i = 0; i < Data.dataNum; i++) {
			labelIndex[i] = i;
		}
		
		for (int i = 0; i < Data.featureNum; i++) {
			double interval = 0;
			Data.setInterval(i);
			if (!Data.isDiscrete) { interval = calculInterval(i); }
			
			chiTable = new int[Data.intervalNum][labelCount];
			if (Data.isDiscrete) { makeChiTable(i, labelCount); }
			else { makeChiTable(i, labelCount, interval); }
			chiSquare[i][0] = calculChisq(labelCount);
			chiSquare[i][1] = i;
		}
		
		quickSort(chiSquare, 0, Data.featureNum - 1);
		for (int i = 0; i < Data.featureNum; i++) {
			bestFeature[i] = (int)chiSquare[i][1];
		}
		Data.setBestFeature(bestFeature);
		for (int i = 0; i < Data.featureNum; i++) {
			//System.out.printf("Feature %d : %.6f\n", (int)chiSquare[i][1], chiSquare[i][0]);
			if (chiSquare[i][0] < minChi) {
				return i;
			}
		}
		return Data.featureNum - 1;
	}

	private static double calculInterval (int index) {
		min = Double.POSITIVE_INFINITY;
		max = Double.NEGATIVE_INFINITY;
		
		for (int i = 0; i < Data.dataNum; i++) {
			if (Data.feature[i][index] < min) { min = Data.feature[i][index]; }
			if (Data.feature[i][index] > max) { max = Data.feature[i][index]; }
		}
		
		return (max - min) / Data.intervalNum;
	}
	
	private static void makeChiTable (int featureNum, int labelCount) {
		for (int i = 0; i < Data.intervalNum; i++) {
			for (int j = 0; j < labelCount; j++) {
				chiTable[i][j] = 0;
			}
		}
		double[] featureTemp = new double[Data.dataNum];
		for (int i = 0; i < Data.dataNum; i++) {
			featureTemp[i] = Data.feature[i][featureNum];
		}
		Arrays.sort(featureTemp);
		
		int index = 0;
		double previous = featureTemp[0];
		for (int i = 0; i < Data.dataNum; i++) {
			if (featureTemp[i] != previous) {
				index++;
			}
			chiTable[index][Data.label[i] - 1]++;
		}
	}
	
	private static void makeChiTable (int featureNum, int labelCount, double interval) {
		for (int i = 0; i < Data.intervalNum; i++) {
			for (int j = 0; j < labelCount; j++) {
				chiTable[i][j] = 0;
			}
		}
		//distribute data to proper table location
		for (int i = 0; i < Data.dataNum; i++) {
			int dataFeatureLoca = (int)((Data.feature[i][featureNum] - min) / interval);
			if (dataFeatureLoca == Data.intervalNum) { dataFeatureLoca--; }
			chiTable[dataFeatureLoca][Data.label[i] - 1]++;
		}
	}
	
	private static double calculChisq (int labelUnit) {
		double a, r, c, n, e, result = 0;
		/**
		 * a : no. patterns in the ith interval(feature), jth class(label)
	     * r : no. patterns in the ith interval
	     * c : no. patterns in the jth class
	     * n : total no. patterns
	     * e : expected frequency of a == r * c / n
	     */
		n = Data.dataNum;
		
		for (int i = 0; i < Data.intervalNum; i++) {
			r = 0;
			for (int j = 0; j < labelUnit; j++) {
				r += chiTable[i][j];
			}
			for (int j = 0; j < labelUnit; j++) {
				a = chiTable[i][j];
				c = 0;
				for (int k = 0; k < Data.intervalNum; k++) {
					c += chiTable[k][j];
				}
				e = r * c / n;
				
				if (r == 0 || c == 0) { e = 0.1; }
				
				result += Math.pow(a - e, 2) / e;
			}
		}
		return result;
	}
	
	public static void quickSort (double[][] arr, int left, int right) {
		if (left == right) { return; }
		double pivotValue = arr[left][0];
		int pivot = (int)arr[left][1], lHold = left, rHold = right;
		
		while (left < right) {
			while ((arr[right][0] <= pivotValue) && (left < right)) { right--; }
			if (left != right) {
				arr[left][0] = arr[right][0];
				arr[left][1] = arr[right][1];
				left++;
			}
			while ((arr[left][0] >= pivotValue) && (left < right)) { left++; }
			if (left != right) {
				arr[right][0] = arr[left][0];
				arr[right][1] = arr[left][1];
				right--;
			}
		}
		arr[left][0] = pivotValue;
		arr[left][1] = pivot;
		pivot = left;
		left = lHold;
		right = rHold;
		if (left < pivot) { quickSort(arr, left, pivot - 1); }
		if (right > pivot) { quickSort(arr, pivot + 1, right); }
	}
}
