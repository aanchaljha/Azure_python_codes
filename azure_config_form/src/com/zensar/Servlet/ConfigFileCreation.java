package com.zensar.Servlet;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import org.apache.log4j.Logger;


 /* @author Aanchal*/
 
  @WebServlet("/ConfigFileCreation")
public class ConfigFileCreation extends HttpServlet {
	final static Logger logger = Logger.getLogger(ConfigFileCreation.class);
	private static final long serialVersionUID = 1L;

	public ConfigFileCreation() {
		super();
	}

	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}

	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		HttpSession session = request.getSession();

		String Source = request.getParameter("Source");
		System.out.println("Source:" + Source);
		String Target = request.getParameter("Target");
		System.out.println("Target:" + Target);

		String filename = Source + "To" + Target;

		session.setAttribute("sourceVal", Source);
		session.setAttribute("targetVal", Target);

		File file = new File("/home/zensar/Config_data/" + filename + ".cfg");

		System.out.println("file converted");

		FileWriter fw = new FileWriter(file.getAbsoluteFile(), true);

		if ((Source.equals("Blob") && Target.equals("Blob"))) {
			logger.info("Blob to Blob has been selected");
			logger.debug("configuration file " + filename + " created");
			request.getRequestDispatcher("BlobToBlob.jsp").forward(request, response);

		} else if ((Source.equals("CSV") && Target.equals("Table"))) {
			System.out.println("in csv table");
			logger.info("CSV to Table has been selected");
			logger.debug("configuration file " + filename + " created");
			request.getRequestDispatcher("GetAzureSqlTable").forward(request, response);

		} else if ((Source.equals("Table") && Target.equals("Table"))) {
			System.out.println("table to table");
			logger.info("Table to Table has been selected");
			logger.debug("configuration file " + filename + " created");
			request.getRequestDispatcher("GetAzureSqlTable").forward(request, response);
		} else {
			System.out.println("Source/Target not found");
			logger.info("Source ang Target you selected is not valid");
		}

		fw.close();
	}

}
