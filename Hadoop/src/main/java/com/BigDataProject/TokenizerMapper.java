package com.BigDataProject;

import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

public class TokenizerMapper extends Mapper<Object, Text, Text, FloatWritable>{

    private final static FloatWritable writeScore = new FloatWritable(1);
    private Text tennis = new Text();

    @SuppressWarnings("unchecked")
    public void map(Object key, Text value, @SuppressWarnings("rawtypes") Mapper.Context context) throws IOException, InterruptedException {
        String row = value.toString();
        String[] cols = row.split(",");
        String PlayerName1 = cols[1];
        String[] score= cols[4].split(" ");
        int SetNumber = score.length ;
        float Player1Sum =0;
        float Player2Sum =0;
        for ( int i=0 ; i<SetNumber ; i++){
            String[] SetScore = score[i].split("-");
            Player1Sum = Player1Sum +  Float.parseFloat(SetScore[0]);
            Player2Sum =  Player2Sum + Float.parseFloat(String.valueOf(SetScore[1].charAt(0)));
        }
        float Player1_cout = Player1Sum /  SetNumber ;
        float Player2_cout = Player2Sum /  SetNumber ;
        String PlayerName2 = cols[3];
        tennis.set(PlayerName1);
        writeScore.set(Player1_cout);
        context.write(tennis, writeScore);
        tennis.set(PlayerName2);
        writeScore.set(Player2_cout);
        context.write(tennis, writeScore);
    }
}
