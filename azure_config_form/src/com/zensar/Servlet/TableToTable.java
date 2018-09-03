package com.zensar.Servlet;

import java.io.BufferedWriter;
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

@WebServlet("/TableToTable")
public class TableToTable extends HttpServlet {
	final static Logger logger = Logger.getLogger(TableToTable.class);

	private static final long serialVersionUID = 1L;

	
	public TableToTable() {
		super();
	}

	
	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}

	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {

		HttpSession session = request.getSession();


		String pipeline_name = request.getParameter("pipeline_name");
		String act_name = request.getParameter("act_name");
		String dataset_input = request.getParameter("dataset_input");
		String dataset_output = request.getParameter("dataset_output");
		String linkedserviceinput = request.getParameter("linkedserviceinput");
		String linkedserviceoutput = request.getParameter("linkedserviceoutput");
		String activity_desc = request.getParameter("activity_desc");

		String Source = (String) session.getAttribute("sourceVal");
		System.out.println("Servlet Source:" + Source);
		String Target = (String) session.getAttribute("targetVal");
		System.out.println("Servlet Target:" + Target);
		String filename = Source + "To" + Target;

		File file = new File("/home/zensar/Config_data/" + filename + ".cfg");
		FileWriter fw = new FileWriter(file.getAbsoluteFile());
		BufferedWriter bw = new BufferedWriter(fw);
		bw.write("[CONNECTION]");
		bw.write("\nsubscription_id=''");
		bw.write("\nrg_name=''");
		bw.write("\ndf_name=''");
		bw.write("\nclient_id=''");
		bw.write("\nsecret=''");
		bw.write("\ntenant=''");
		bw.write("\nstorage_account_details=''");
		bw.write("\nazureSqlConnString=''");
		bw.write("\nmysqlConnString=''");

		bw.write("\np_name=" + pipeline_name);
		bw.write("\nact_name=" + act_name);
		bw.write("\ndsIn_name=" + dataset_input);
		bw.write("\ndsOut_name=" + dataset_output);
		bw.write("\nls_name=" + linkedserviceinput);
		bw.write("\nls_name1=" + linkedserviceoutput);
		bw.write("\nintegrationRuntime=integrationRuntime1");
		bw.write("\nRetry=0");
		bw.write("\nRetry Interval=1");
		bw.write("\nact_description=" + activity_desc);
		logger.info("Input has been written into the "+ filename + ".cfg");
		bw.close();

		request.setAttribute("filename", filename);

		request.getRequestDispatcher("PythonCodeCaller").forward(request, response);

	}
}
