public static double[] addVectors(double[] v1, double[] v2) {
    double[] result = new double[v1.length];

    for (int i = 0; i < v1.length; i++) {
        result[i] = v1[i] + v2[i];
    }

    return result;
}

public static double[] mulVectorNumber(double[] v1, double num) {
    double[] result = new double[v1.length];

    for (int i = 0; i < v1.length; i++) {
        result[i] = v1[i] * num;
    }

    return result;
}


public static boolean contains(int[] v1, double featureRef) {
    return Arrays.binarySearch(v1, (int)featureRef) >= 0;
}

public static int[] parseIntArray(String input) {
    String[] strings = input.split(",");
    int[] numbers = new int[strings.length];
    for (int i = 0; i < numbers.length; i++)
    {
        numbers[i] = Integer.parseInt(strings[i]);
    }
    Arrays.sort(numbers);
    return numbers;
}
