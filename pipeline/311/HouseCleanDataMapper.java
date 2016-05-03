package house_rent;

import java.io.IOException;
import java.lang.Object;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class HouseCleanDataMapper 
	extends Mapper<Object, Text, Text, Text> {
	
	@Override
	public void map(Object key, Text value, Context context)
			throws IOException, InterruptedException {
		String raw = value.toString().toLowerCase();
		String[] line = raw.split("\t");
		for(int i = 0; i < line.length; i++){
			if (line[5].equals("new york")){
				line[5] = "manhattan";
			}
			if (line[3].indexOf("heat")>=0){
				line[3] = "heating";
			}else if(line[3].indexOf("noise")>=0){
				line[3] = "noise";
			}else if(line[3].equals("plumbing")){
				line[3] = "plumbing";
			}else if(line[3].indexOf("general construction")>=0){
				line[3] = "general construction";
			}else if(line[3].indexOf("paint")>=0){
				line[3] = "paint/plaster";
			}else if(line[3].indexOf("blocked driveway")>=0){
				line[3] = "blocked driveway";
			}else if(line[3].indexOf("street")>=0){
				line[3] = "street condition";
			}else if(line[3].indexOf("parking")>=0){
				line[3] = "illegal parking";
			}else if(line[3].indexOf("water")>=0){
				line[3] = "water condition";
			}else if(line[3].indexOf("electric")>=0){
				line[3] = "electric";
			}else if(line[3].indexOf("sani") >=0 | line[3].indexOf("dirty")>=0 ){
				line[3] = "unsanitary condition";
			}else if(line[3].indexOf("rodent")>=0){
				line[3] = "rodent";
			}else if(line[3].indexOf("sewer")>=0){
				line[3] = "sewer";
			}else if(line[3].indexOf("tree")>=0){
				line[3] = "damaged tree";
			}else{
				line[3] = "other";
			}
		}

		String resultline = line[1];
		
		for(int i = 2; i < 10; i++){
			resultline += "\t" + line[i];
		}
		context.write(new Text(line[0]), new Text(resultline));
	}
}
