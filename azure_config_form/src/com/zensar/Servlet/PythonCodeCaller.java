package com.zensar.Servlet;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import org.apache.log4j.Logger;

@WebServlet("/PythonCodeCaller")
public class PythonCodeCaller extends HttpServlet {
	final static Logger logger = Logger.getLogger(PythonCodeCaller.class);
	private static final long serialVersionUID = 1L;

	public PythonCodeCaller() {
		super();
	}

	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}

	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		HttpSession session = request.getSession();
		try {

			String filename = (String) request.getAttribute("filename");
			System.out.println("filename: " + filename);
			if (filename.equals("BlobToBlob")) {
				logger.debug("Now pipeline for BlobToBlob will be executed ");

				String pythonScriptPath = "/home/zensar/Config_data/BlobToBlob.py";
				String[] cmd = new String[2];
				cmd[0] = "/usr/bin/python3.5";
				cmd[1] = pythonScriptPath;

				ProcessBuilder pb = new ProcessBuilder(cmd[0],cmd[1]);
				@SuppressWarnings("unused")
				Process p = pb.start();

				// create runtime to execute external command
				Runtime rt = Runtime.getRuntime();
				Process pr = rt.exec(cmd);

				// retrieve output from python script
				BufferedReader bfr1 = new BufferedReader(new InputStreamReader(pr.getInputStream()));
				String line = "";
				logger.debug("Source:" + session.getAttribute("sourceVal"));
				logger.debug("Target:" + session.getAttribute("targetVal"));
				logger.debug("Configuration filename:" + filename + ".cfg");
				while ((line = bfr1.readLine()) != null) {
					// display each output line form python script
					System.out.println(line);

					logger.debug("output:" + line);

				}
				logger.debug("Execution for pipeline " + filename + " has finished");
				response.sendRedirect("Execute.jsp");
			}
			else if (filename.equals("CSVToTable")) {
				logger.debug("Now pipeline for CSVtoTable will be executed ");
				String pythonScriptPath = "/home/zensar/Config_data/CSVtoTable.py";
				String[] cmd = new String[2];
				cmd[0] = "/usr/bin/python3.5"; // check version of installed python: python -V
				cmd[1] = pythonScriptPath;

				ProcessBuilder pb = new ProcessBuilder("/usr/bin/python3.5", pythonScriptPath);
				@SuppressWarnings("unused")
				Process p = pb.start();

				// create runtime to execute external command
				Runtime rt = Runtime.getRuntime();
				Process pr = rt.exec(cmd);

				// retrieve output from python script
				BufferedReader bfr1 = new BufferedReader(new InputStreamReader(pr.getInputStream()));
				String line = "";
				logger.debug("Source:" + session.getAttribute("sourceVal"));
				logger.debug("Target:" + session.getAttribute("targetVal"));
				logger.debug("Configuration filename:" +filename+ ".cfg");
				while ((line = bfr1.readLine()) != null) {
					// display each output line form python script
					System.out.println(line);

					logger.debug("output:" + line);

				}
				logger.debug("Execution for pipeline " + filename + " has finished");
				response.sendRedirect("Execute.jsp");

			}

			else if (filename.equals("TableToTable")) {
				logger.debug("Now pipeline for TabletoTable will be executed ");
				String pythonScriptPath = "/home/zensar/Config_data/TabletoTable.py";
				String[] cmd = new String[2];
				cmd[0] = "/usr/bin/python3.5"; // check version of installed python: python -V
				cmd[1] = pythonScriptPath;
				System.out.println("executing pcode");

				ProcessBuilder pb = new ProcessBuilder("/usr/bin/python3.5", pythonScriptPath);
				@SuppressWarnings("unused")
				Process p = pb.start();

				// create runtime to execute external command
				Runtime rt = Runtime.getRuntime();
				Process pr = rt.exec(cmd);
				
				// retrieve output from python script
				BufferedReader bfr1 = new BufferedReader(new InputStreamReader(pr.getInputStream()));
				String line = "";
				logger.debug("Source:" + session.getAttribute("sourceVal"));
				logger.debug("Target:" + session.getAttribute("targetVal"));
				logger.debug("Configuration filename:" + filename + ".cfg");
				while ((line = bfr1.readLine()) != null) {
					// display each output line form python script
					System.out.println(line);

					logger.debug("output:" + line);

				}
				logger.debug("Execution for pipeline " + filename + " has finished");
				response.sendRedirect("Execute.jsp");

			} else {
				System.out.println("source not found !");
				logger.info("source not found !");
			}

		} catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
			logger.info("Not executed");

		}

	}

}
