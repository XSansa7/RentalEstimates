package house_rent;
import java.io.IOException;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class HouseCleanDataReducer extends
	Reducer<Text, Text, Text, Text >{
	
	@Override
	public void reduce(Text key, Iterable<Text> values, Context context)
		throws IOException, InterruptedException{
		
		String result = new String();
		
		for(Text value : values){
			result = value.toString();
		}
		context.write(key, new Text(result));
	}
}