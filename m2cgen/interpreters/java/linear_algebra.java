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


public static boolean contains(MinBitset v1, double featureRef) {
    return v1.contains((int) featureRef);
}

public static MinBitset parseIntArray(String input) {
    String[] strings = input.split(",");
    int[] numbers = new int[strings.length];
    for (int i = 0; i < strings.length; i++) {
        numbers[i] = Integer.parseInt(strings[i]);
    }
    return new MinBitset(numbers);
}


public static class MinBitset {

    private final int offset;
    private final BitSet set;

    // Inspired by TreeLite which uses bitmaps to deal with categorical variables. This is ~3x faster vs HashSet<Integer>
    // https://github.com/dmlc/treelite/blob/46c8390aed4491ea97a017d447f921efef9f03ef/src/compiler/common/categorical_bitmap.h#L22-L28
    public MinBitset(int[] input) {
        Arrays.sort(input);

        // offset the values by the minimum. this helps with memory usage for ranges that start high
        offset = input[0];
        int max = input[input.length - 1];

        set = new BitSet(max - offset);

        for (int value : input) {
            int categorical = value - offset;
            set.set(categorical);
        }
    }

    public boolean contains(int value) {
        value -= offset;
        if (value > -1) {
            return set.get(value);
        }
        return false;
    }
}
