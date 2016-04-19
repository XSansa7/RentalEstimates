import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.PriorityQueue;
import java.util.StringTokenizer;

public class processor {
	
	public static void main(String argv[]) {
		if (argv.length != 1) {
			System.err.println("Usage: java processor DOCS_PATH");
		}
		
		String docsPath = argv[0];
		final File folder = new File(docsPath);
		if (!folder.isDirectory()) {
			System.out.println("Invalid path name " + docsPath);
			System.exit(1);
		}
		
		for (File entry : folder.listFiles()) {
			int temp = entry.getName().lastIndexOf("_");
			if (!entry.getName().substring(temp + 1).equals("zpid")) {
				continue;
			}
			InputStream is;
		    try {
		    	String line = entry.getName();
				is = new FileInputStream(entry);
			    byte b[] = new byte[1000];
			    int numRead;
				numRead = is.read(b);
			    String content = new String(b, 0, numRead);
			    while ((numRead != -1)) {
				    numRead = is.read(b);
				    if (numRead != -1) {
					    String newContent = new String(b, 0, numRead);
					    content += newContent;
				    }
			    }
			    int markAddr = content.indexOf("<meta property=\"og:zillow_fb:address\" content=\"");
			    String address = "unknown";
			    String street = "unknown";
			    String city = "unknown";
			    String state = "unknown";
			    String zipcode = "unknown";
			    if (markAddr != -1) {
			        //System.out.println(markAddr);
			        //System.out.println(content.substring(markAddr, markAddr + "<meta property=\"og:zillow_fb:address\" content=\"".length()));
			        int closeAddr = content.indexOf("\"", markAddr + "<meta property=\"og:zillow_fb:address\" content=\"".length());
			        //System.out.println(closeAddr);
			        address = content.substring(markAddr + "<meta property=\"og:zillow_fb:address\" content=\"".length(), closeAddr);
			        String[] comp = address.split(", ");
			        street = comp[0];
			        city = comp[1];
			        String[] comp2 = comp[2].split(" ");
			        state = comp2[0];
			        zipcode = comp2[1];
			    }
			    line += "\t" + address;
			    line += "\t" + street;
			    line += "\t" + city;
			    line += "\t" + state;
			    line += "\t" + zipcode;
                int markBeds = content.indexOf("<span class=\"addr_bbs\">");
			    //int markBeds = content.indexOf("<meta property=\"zillow_fb:beds\" content=\"");
			    String beds = "unknown";
			    if (markBeds != -1) {
			    	//int closeBeds = content.indexOf("\"", markBeds + "<meta property=\"zillow_fb:beds\" content=\"".length() + 1);
			    	int closeBeds = content.indexOf("<", markBeds + "<span class=\"addr_bbs\">".length());
			    	//if (closeBeds != -1) {
			    	//beds = content.substring(markBeds + "<meta property=\"zillow_fb:beds\" content=\"".length(), closeBeds);
			    		beds = content.substring(markBeds + "<span class=\"addr_bbs\">".length(), closeBeds);
			    	//}
			    	//else {
			    	//	int iTemp = content.indexOf("<", markBeds + "<span class=\"addr_bbs\">".length());
			    	//	beds = content.substring(markBeds + "<span class=\"addr_bbs\">".length(), iTemp);
			    	//}
			    }
			    line += "\t" + beds;
			    int markBaths = content.indexOf("<span class=\"addr_bbs\">", markBeds + "<span class=\"addr_bbs\">".length());
			    //int markBaths = content.indexOf("<meta property=\"zillow_fb:baths\" content=\"", markBeds + "<span class=\"addr_bbs\">".length());
			    String baths = "unknown";
			    if (markBaths != -1) {
			    	int closeBaths = content.indexOf("<", markBaths + "<span class=\"addr_bbs\">".length());
			    	//int closeBaths = content.indexOf("\"", markBaths + "<meta property=\"zillow_fb:baths\" content=\"".length() + 1);
			    	//baths = content.substring(markBaths + "<meta property=\"zillow_fb:baths\" content=\"".length(), closeBaths);
			    	baths = content.substring(markBaths + "<span class=\"addr_bbs\">".length(), closeBaths);
			    }
			    line += "\t" + baths;
			    int markSpace = content.indexOf("<span class=\"addr_bbs\">", markBaths + "<span class=\"addr_bbs\">".length());
			    String space = "unknown";
			    String space_number = "-1";
			    if (markSpace != -1) {
			    	int closeSpace = content.indexOf("<", markSpace + "<span class=\"addr_bbs\">".length());
			    	space = content.substring(markSpace + "<span class=\"addr_bbs\">".length(), closeSpace);
			    	String temp2 = space.substring(0, space.indexOf("sqft") - 1);
			    	if (!temp2.equals("--")) {
			    	    space_number = temp2.replace(",", "");		
			    	}
			    }
			    System.err.println(space);
			    line += "\t" + space;
			    int markSold = content.indexOf("<span id=\"listing-icon\" data-icon-class=\"zsg-icon-recently-sold\" class=\"zsg-icon-recently-sold recently-sold\"></span>  Sold: <span class=\"\">");
			    String sold = "unknown";
			    String sold_number = "-1";
			    if (markSold != -1) {
			    	int closeSold = content.indexOf("<", markSold + "<span id=\"listing-icon\" data-icon-class=\"zsg-icon-recently-sold\" class=\"zsg-icon-recently-sold recently-sold\"></span>  Sold: <span class=\"\">".length() + 1);
			        sold = content.substring(markSold + "<span id=\"listing-icon\" data-icon-class=\"zsg-icon-recently-sold\" class=\"zsg-icon-recently-sold recently-sold\"></span>  Sold: <span class=\"\">".length(), closeSold);
			        sold_number = sold.replace(",", "");
			    	sold_number = sold_number.replace("$", "");
			    }
			    
			    line += "\t" + sold;
			    int markSale = content.indexOf("<span id=\"listing-icon\" data-icon-class=\"zsg-icon-for-sale\" class=\"zsg-icon-for-sale for-sale\"></span>");
			    String sale = "unknown";
			    String sale_number = "-1";
			    if (markSale != -1) {
			    	int iStart = content.indexOf("<div class=\"main-row  home-summary-row\">   <span class=\"\">", markSale);
			    	int closeSale = content.indexOf("<", iStart + "<div class=\"main-row  home-summary-row\">   <span class=\"\">".length());
			    	sale = content.substring(iStart + "<div class=\"main-row  home-summary-row\">   <span class=\"\">".length(), closeSale);
			    	sale_number = sale.replace(",", "");
			    	sale_number = sale_number.replace("$", "");
			    }
			    line += "\t" + sale;
			    int markRental = content.indexOf("<span id=\"listing-icon\" data-icon-class=\"zsg-icon-for-rent\" class=\"zsg-icon-for-rent for-rent\"></span>");
			    String rent = "unknown";
			    if (markRental != -1) {
			    	int iStart = content.indexOf("<div class=\"main-row  home-summary-row\">   <span class=\"\">", markRental);
			    	int closeRent = content.indexOf("<", iStart + "<div class=\"main-row  home-summary-row\">   <span class=\"\">".length());
			    	rent = content.substring(iStart + "<div class=\"main-row  home-summary-row\">   <span class=\"\">".length(), closeRent);
			    }
			    line += "\t" + rent;
			    int markFact = content.indexOf("<h3 class=\"zsg-content_collapsed zsg-h4\">Facts</h3>");
			    String lot = "unknown";
			    String soldDate = "unknown";
			    String builtDate = "unknown";
			    if (markFact != -1) {
			    	int markLot = content.indexOf("<li>Lot: ", markFact);
			    	if (markLot != -1) {
			    		int closeLot = content.indexOf("<", markLot + "<li>Lot: ".length());
			    		lot = content.substring(markLot + "<li>Lot: ".length(), closeLot);
			    	}
			    	int markSoldDate = content.indexOf("<li>Last sold: ", markFact);
			    	if (markSoldDate != -1) {
			    		int closeSoldDate = content.indexOf("<", markSoldDate + "<li>Last sold: ".length());
			    		soldDate = content.substring(markSoldDate + "<li>Last sold: ".length(), closeSoldDate);
			    	}
			    	int markBuiltDate = content.indexOf("<li>Built in ", markFact);
			    	if (markBuiltDate != -1) {
			    		int closeBuiltDate = content.indexOf("<", markBuiltDate + "<li>Built in ".length());
			    		builtDate = content.substring(markBuiltDate + "<li>Built in ".length(), closeBuiltDate);			    		
			    	}
			    }
			    int markFeature = content.indexOf("<h3 class=\"zsg-content_collapsed zsg-h4\">Features</h3>");
			    String parking = "unknown";
			    if (markFeature != -1) {
			    	int markParking = content.indexOf("<li>Parking: ", markFeature);
			    	if (markParking != -1) {
			    		int closeParking = content.indexOf("<", markParking + "<li>Parking: ".length());
			    		parking = content.substring(markParking + "<li>Parking: ".length(), closeParking);
			    	}
			    }
			    line += "\t" + lot;
			    line += "\t" + soldDate;
			    line += "\t" + builtDate;
			    line += "\t" + parking;
			    System.out.println(line);
			    
			} catch (Exception e) {
			// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	    
	}

}
