package com.zensar.Servlet;

import java.io.IOException;
import javax.servlet.http.HttpSession;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.log4j.Logger;


@WebServlet("/GetAzureSqlTable")
public class GetAzureSqlTable extends HttpServlet {
	final static Logger logger = Logger.getLogger(GetAzureSqlTable.class);
	private static final long serialVersionUID = 1L;

	
	public GetAzureSqlTable() {
		super();
	}

	protected void service(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		ArrayList<String> arrayList = new ArrayList<String>();
		HttpSession session = request.getSession();

		String url = String.format("");
		logger.debug("Connected to Azure SQL Server Database");
		Connection connection = null;
		ResultSet resultSet = null;
		Statement statement = null;

		try {
			Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
			connection = DriverManager.getConnection(url);
			String sql = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'";

			statement = connection.createStatement();
			resultSet = statement.executeQuery(sql);
			while (resultSet.next()) {
				arrayList.add(resultSet.getString(1));
			}
			String Source = (String) session.getAttribute("sourceVal");
			System.out.println(Source);

			String Target = (String) session.getAttribute("targetVal");
			System.out.println(Target);

			session.setAttribute("listTables", arrayList);
			if ((Source.equals("CSV") && Target.equals("Table"))) {
				request.getRequestDispatcher("CSVToTable.jsp").forward(request, response);
			} else if ((Source.equals("Table") && Target.equals("Table"))) {

				request.getRequestDispatcher("TableToTable.jsp").forward(request, response);
			}

		}

		catch (Exception e) {
			System.out.println("Exception " + e.getMessage());
			logger.info(e.getMessage());
			e.printStackTrace();
		} finally {
			try {
				connection.close();
				logger.info("connection has been closed");
			} catch (SQLException e) {
				e.printStackTrace();
			}
		}
	}

}
