<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Zen_analytica</title>
<script src="js/mui.min.js"></script>
<link rel="stylesheet" type="text/css" href="css/mui.css" />
<link rel="stylesheet" type="text/css" href="css/bootstrap.min.css" />


</head>
<body>

	<div class="mui-appbar">
		<a href="index1.jsp" title="Index"> <img
			src="img/zen_analytica_logo_text.png"
			style="padding-left: 15px; width: 170px; padding-top: 15px"
			alt="zen analytica Logo" />
		</a>

	</div>

	<div class="s">
		<ul class="mui-tabs__bar mui-tabs__bar--justified">
			<li class="mui--is-active"><a data-mui-toggle="tab"
				data-mui-controls="pane-justified-1">source and target</a></li>
			<li><a data-mui-toggle="tab"
				data-mui-controls="pane-justified-2">set properties</a></li>
			<li><a data-mui-toggle="tab"
				data-mui-controls="pane-justified-3">execute pipeline</a></li>
		</ul>
		<div class="mui-tabs__pane mui--is-active" id="pane-justified-1">
			<div class="row">
				<form action="ConfigFileCreation" method="post" class="mui-form"
					style="align-content: center;">
					<br> <br>
					<div class="mui-dropdown">

						<select required class="mui-btn mui-btn--primary"
							style="align-items: center;" data-mui-toggle="dropdown"
							name="Source" id="Source" required>
							<option value="#">Select Source</option>
							<option value="Blob">Blob</option>
							<option value="CSV">CSV</option>
							<option value="Table">Table</option>
							<option value="My sql">My sql</option>
							<option value="Log">Log</option>
							<option value="Tweeter feed">Tweeter feed</option>
						</select>
					</div>
					<div class="mui-dropdown">
						<select required class="mui-btn mui-btn--primary"
							data-mui-toggle="dropdown" name="Target" id="Target" required>
							<option value="#">Select Target</option>
							<option value="Blob">Blob</option>
							<option value="Table">Table</option>
							<option value="Table">Table</option>
							<option value="Text">Text</option>
							<option value="sql DW">sql DW</option>
							<option value="Log">Log</option>

						</select>
					</div>
					<br>

					<button type="submit" name="generate" id="generate" value="Execute"
						class="mui-btn mui-btn--raised">Next</button>
				</form>
			</div>
		</div>
	</div>
</body>
</html>