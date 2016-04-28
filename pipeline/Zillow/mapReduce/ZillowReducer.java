import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class ZillowReducer 
        extends Reducer<Text, Text, Text, Text> {

    @Override
    public void reduce(Text key, Iterable<Text> values, Context context) 
            throws IOException, InterruptedException {
        String v = "";
        for (Text value : values) {
            v = value.toString(); 
        }
        context.write(key, new Text(v));
    }
}

