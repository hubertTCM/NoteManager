package com.hubert.tcm.util;

import android.view.*;

public class Util {

    public static boolean isNullOrEmpty(String str){
        return str == null || str.isEmpty();
    }
    
    public static String convert(double value){
        if (value - (int)value > 0){
            return Double.toString(value);
        }
        return Integer.toString((int)value);
    }
    
    public static View getLastChild(ViewGroup parent){
        int count = parent.getChildCount();
        if (count <= 0){
            return null;
        }
        return parent.getChildAt(count - 1);
    }
}
