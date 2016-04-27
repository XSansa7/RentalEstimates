import java.io.IOException;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class ZillowMapper 
        extends Mapper<LongWritable, Text, Text, Text> {
	@Override
	public void map(LongWritable key, Text value, Context context)
	        throws IOException, InterruptedException {
		
		String line = value.toString();
		String comp[] = line.split("\t");
                System.out.println(comp.length);
		String zpid = comp[0];
		String addr = comp[1];
		String beds_info = comp[6];
		String baths_info = comp[7];
		String size_info = comp[8];
		String prev_price_info = comp[9];
		String curr_price_info = comp[10];
		String rent = comp[11];
		String lot_size_info = comp[12];
		String transaction = comp[13];
		String built_time = comp[14];
		/*String parking_size = comp[15];*/
		
		String num_of_beds = beds_info.split(" ")[0];
		String num_of_baths = baths_info.split(" ")[0];
		String size;
		int temp = size_info.indexOf("sqft");
		if (temp != -1) {
			size = size_info.substring(0, temp - 1).replaceAll(",", "");
		}
		else {
			int temp2 = size_info.indexOf("acre");
			if (temp2 != -1) {
				size = size_info.substring(0, temp2 - 1).replaceAll(",", "");
				if (size.contains(".")) {
					size = Double.toString(Double.parseDouble(size) * 43560);
				}
				else {
					size = Integer.toString(Integer.parseInt(size) * 43560);
				}
			}
			else {
				size = size_info.replaceAll(",", "");
			}
		}
		
	        /*String prev_price;
		if (!prev_price_info.equals("unknown")) {
			prev_price = prev_price_info.replace("$", "");
			prev_price.replace(",", "");
		}
		else {
			prev_price = prev_price_info;
		}*/
		String curr_price;
		if (!curr_price_info.equals("unknown")) {
                        int temp0 = curr_price_info.indexOf("$");
			curr_price = curr_price_info.substring(temp0 + 1);
                        curr_price = curr_price.replaceAll(",", "");
		}
		else {
			curr_price = curr_price_info;
		}
		
	        String lot_size;
		int temp3 = lot_size_info.indexOf("sqft");
		if (temp3 != -1) {
			lot_size = lot_size_info.substring(0, temp3 - 1).replaceAll(",", "");
		}
		else {
			int temp4 = lot_size_info.indexOf("acre");
			if (temp4 != -1) {
				lot_size = lot_size_info.substring(0, temp4 - 1).replaceAll(",", "");
				if (lot_size.contains(".")) {
					lot_size = Double.toString(Double.parseDouble(lot_size) * 43560);
					}
				else {
					lot_size = Integer.toString(Integer.parseInt(lot_size) * 43560);
				}
			}
			else {
				lot_size = lot_size_info.replaceAll(",", "");
			}
		}
		
		String trans_price;
		String trans_month;
		String trans_year;
		int month;
		int trans_time;
		if (!transaction.equals("unknown")) {
			trans_month = transaction.split(" ")[0];
			switch (trans_month) {
				case "Jan": month = 1;
					break;
				case "Feb": month = 2;
					break;
				case "Mar": month = 3;
					break;
				case "Apr": month = 4;
					break;
				case "May": month = 5;
					break;
				case "Jun": month = 6;
					break;
				case "Jul": month = 7;
					break;
				case "Aug": month = 8;
					break;
				case "Sep": month = 9;
					break;
				case "Oct": month = 10;
					break;
				case "Nov": month = 11;
					break;
				case "Dec": month = 12;
					break;
				default: month = 0;
				    break;			
			}
			trans_year = transaction.split(" ")[1];
			int year = Integer.parseInt(trans_year);
			if (month != 0) {
				trans_time = (2016 - year) * 12 + (5 - month);
			}
			else {
				trans_time = -1;
			}
                        int temp4 = transaction.split(" ")[3].indexOf("$");
			trans_price = transaction.split(" ")[3].substring(temp4 + 1).replaceAll(",", "");
		}
		else {
			trans_price = "unknown";
			trans_time = -1;			
		}
		
		String price;
		int time;
		if (!curr_price.equals("unknown")) {
			price = curr_price;
			time = 0;
		}
		else {
			price = trans_price;
			time = trans_time;
		}
		
		/*int parking = -1;
		if (!parking_size.equals("unknown")) {
			String[] comp1 = parking_size.split(" ");
			for (int i = 0; i < comp1.length; i++) {
				if (comp1[i].toLowerCase().contains("street") || comp1[i].toLowerCase().equals("public")) {
					parking = 0;
					break;
				}
			}
			for (int i = 0; i < comp1.length; i++) {
				if (comp1[i].toLowerCase().contains("tached") || comp1[i].toLowerCase().equals("carport")) {
					parking = 1;
				}
			}
			for (int i = 0; i < comp1.length; i++) {
				if (comp1[i].toLowerCase().equals("none") || comp1[i].toLowerCase().equals("no") || comp1[i].toLowerCase().equals("0")) {
				parking = 0;
				break;
				}
			}
		}*/
		String v = addr + "\t" + num_of_beds + "\t" + num_of_baths + "\t" + size + "\t" + price + "\t" + time + "\t" + lot_size + "\t" + built_time;
	        context.write(new Text(zpid), new Text(v));
	    
	}	
}
