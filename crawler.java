import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.List;
import java.util.StringTokenizer;

public class crawler {
	public static final String DISALLOW = "Disallow: ";
	
	public static boolean robotSafe(URL url) {
		String strHost = url.getHost();
		
		// form URL of the robots.txt file
		String strRobot = "http://" + strHost + "/robots.txt";
		URL urlRobot;
		try {
			urlRobot = new URL(strRobot);
		} catch (MalformedURLException e) {
			System.err.println("malformed");
			return false;
		}
		
		String strCommands;
		try {
			InputStream urlRobotStream = urlRobot.openStream();
			byte b[] = new byte[1000];
			int numRead = urlRobotStream.read(b);
			strCommands = new String(b, 0, numRead);
			while (numRead != -1) {
				numRead = urlRobotStream.read(b);
				if (numRead != -1) {
					String newCommands = new String(b, 0, numRead);
					strCommands += newCommands;
				}
			}
			urlRobotStream.close();
		} catch (IOException e) {
			return true;
		}
		
		System.out.println(strCommands);
		
		String strURL = url.getFile();
		int index = 0;
		while ((index = strCommands.indexOf(DISALLOW, index)) != -1) {
			index += DISALLOW.length();
			String strPath = strCommands.substring(index);
			StringTokenizer st = new StringTokenizer(strPath);
			
			if (!st.hasMoreTokens()) {
				break;
			}
			
			String strBadPath = st.nextToken();
			//System.err.println(strBadPath);
			
			if (strURL.indexOf(strBadPath) == 0) {
				System.err.println(strBadPath);
				System.err.println(strURL);
				return false;
			}
		}
		return true;
	}
	
	public static String getPage(URL url) {
		try {
			URLConnection urlConnection = url.openConnection();
			urlConnection.setAllowUserInteraction(false);
			
			InputStream urlStream = url.openStream();
			byte b[] = new byte[1000];
			int numRead = urlStream.read(b);
			String content = new String(b, 0, numRead);
			while ((numRead != -1)) {
				numRead = urlStream.read(b);
				if (numRead != -1) {
					String newContent = new String(b, 0, numRead);
					content += newContent;
				}
			}
			return content;
		} catch (IOException e) {
			System.err.println("ERROR: couldn't open URL ");
			return "";
		}
	}
	
	public static void savePage(String page, String filepath, String desPath) {
		//System.out.println("FILENAME: " + filename);
		String path;
		String filename = filepath.substring(filepath.lastIndexOf("/") + 1, filepath.length());
		if (desPath.charAt(desPath.length() - 1) != '/') {
			path = desPath + "/" + filename;
		}
		else {
			path = desPath + filename;
		}
		File f = new File(path);
		if (!f.getParentFile().exists()) {
			f.getParentFile().mkdirs();
		}
		try {
			if (f.createNewFile()) {
			    FileWriter filewriter = new FileWriter(f);
			    filewriter.write(page);
			    filewriter.flush();
			    filewriter.close();
			}
		} catch (IOException e) {
			System.err.println("ERROR: fail to save page ");
			return;
		}
	} 
	
	public static void main(String args[]) {
		if (args.length != 2) {
		    System.err.println("crawler takes 2 argument: url list and destination path");
		    System.exit(1);
		}
		
		
		String urlFileName = args[0];
		File urlFile = new File(urlFileName);
		List<String> urls = null;
		try {
			urls = Files.readAllLines(urlFile.toPath(), StandardCharsets.UTF_8);
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		
		for (int i = 0; i < urls.size(); i++) {
			URL url = null;
			try {
				url = new URL(urls.get(i).trim());
				
			} catch (MalformedURLException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			//if (robotSafe(url)) {
				String page = getPage(url);
			    if (page.length() != 0) {
				    savePage(page, url.getFile(), args[1]);
			  }
		    //}
			//else {
			//	System.err.println("robot exclusion");
			//}
                try {
                    Thread.sleep(5000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
		}
	}				
}


