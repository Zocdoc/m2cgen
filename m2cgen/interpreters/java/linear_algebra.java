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


public static boolean contains(HashSet<Integer> v1, double featureRef) {
    return v1.contains((int) featureRef);
}

public static HashSet<Integer> parseIntArray(String input) {
    String[] strings = input.split(",");
    HashSet<Integer> numbers = new HashSet<Integer>(strings.length);
    for (int i = 0; i < strings.length; i++) {
        numbers.add(Integer.parseInt(strings[i]));
    }
    return numbers;
}
