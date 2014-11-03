package com.hubert.tcm.ui.common;

import android.content.Context;
import android.util.AttributeSet;
import android.view.View;
import android.view.ViewGroup;
import android.widget.*;
 
/**
 *
 * @author RAW
 */
public class WrapLayout extends ViewGroup {
 
    private int lineHeight;
 
    public WrapLayout(Context context) {
        super(context);
    }
 
    public WrapLayout(Context context, AttributeSet attrs) {
        super(context, attrs);
    }
 
    @Override
    protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
        assert (MeasureSpec.getMode(widthMeasureSpec) != MeasureSpec.UNSPECIFIED);
 
        final int width = MeasureSpec.getSize(widthMeasureSpec) - getPaddingLeft() - getPaddingRight();
        int height = MeasureSpec.getSize(heightMeasureSpec) - getPaddingTop() - getPaddingBottom();
        final int count = getChildCount();
        int lineHeight = 0;
 
        int xPosition = getPaddingLeft();
        int yPosition = getPaddingTop();
 
        int childHeightMeasureSpec;
        if (MeasureSpec.getMode(heightMeasureSpec) == MeasureSpec.AT_MOST) {
            childHeightMeasureSpec = MeasureSpec.makeMeasureSpec(height, MeasureSpec.AT_MOST);
        } else {
            childHeightMeasureSpec = MeasureSpec.makeMeasureSpec(0, MeasureSpec.UNSPECIFIED);
        }
 
 
        for (int i = 0; i < count; i++) {
            final View child = getChildAt(i);
            if (child.getVisibility() != GONE) {
                
                final LinearLayout.LayoutParams lp = (LinearLayout.LayoutParams) child.getLayoutParams();
                
                child.measure(MeasureSpec.makeMeasureSpec(width, MeasureSpec.AT_MOST), childHeightMeasureSpec);
                final int childWidth = child.getMeasuredWidth();
                lineHeight = Math.max(lineHeight, child.getMeasuredHeight()); //+ lp.bottomMargin + lp.topMargin; //+ lp.vertical_spacing);
 
                if (xPosition + childWidth > width) {
                    xPosition = getPaddingLeft();
                    yPosition += lineHeight;
                }
 
                xPosition += childWidth + lp.leftMargin + lp.rightMargin; //+ lp.horizontal_spacing;
            }
        }
        this.lineHeight = lineHeight;
 
        if (MeasureSpec.getMode(heightMeasureSpec) == MeasureSpec.UNSPECIFIED) {
            height = yPosition + lineHeight;
 
        } else if (MeasureSpec.getMode(heightMeasureSpec) == MeasureSpec.AT_MOST) {
            if (yPosition + lineHeight < height) {
                height = yPosition + lineHeight;
            }
        }
        setMeasuredDimension(width, height);
    }
 
    @Override
    protected ViewGroup.LayoutParams generateDefaultLayoutParams() {
        //return new LayoutParams(1, 1); // default of 1px spacing
        return new LinearLayout.LayoutParams(1, 1);
    }
 
    @Override
    protected ViewGroup.LayoutParams generateLayoutParams(ViewGroup.LayoutParams p) {
        return p instanceof MarginLayoutParams
                ? new LinearLayout.LayoutParams((MarginLayoutParams) p)
                : new LinearLayout.LayoutParams(p);
    }
    
    @Override
    protected boolean checkLayoutParams(ViewGroup.LayoutParams p){
        return p instanceof LinearLayout.LayoutParams && super.checkLayoutParams(p);
    }
    
    @Override
    public ViewGroup.LayoutParams generateLayoutParams(AttributeSet attrs) {
        return new LinearLayout.LayoutParams(getContext(), attrs);
    }
 
    @Override
    protected void onLayout(boolean changed, int l, int t, int r, int b) {
        final int count = getChildCount();
        final int width = r - l;
        int xpos = getPaddingLeft();
        int ypos = getPaddingTop();
 
        for (int i = 0; i < count; i++) {
            final View child = getChildAt(i);
            if (child.getVisibility() != GONE) {
                final int childw = child.getMeasuredWidth();
                final int childh = child.getMeasuredHeight();
                final LinearLayout.LayoutParams lp = (LinearLayout.LayoutParams) child.getLayoutParams();
                if (xpos + childw + lp.leftMargin > width) {
                    xpos = getPaddingLeft();
                    ypos += lineHeight;
                }
                child.layout(xpos, ypos, xpos + lp.leftMargin + childw, ypos + childh);
                xpos += childw + lp.rightMargin;// + lp.horizontal_spacing;
            }
        }
    }
}
