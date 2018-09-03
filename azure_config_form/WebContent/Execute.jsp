<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Zen_analytica</title>
<script src="//cdn.muicss.com/mui-0.9.39/js/mui.min.js"></script>
<link rel="stylesheet" type="text/css" href="css/mui.css" />

</head>
<body>

	<div class="mui-appbar">
		<a href="index.jsp" title="Index"> <img
			src="img/zen_analytica_logo_text.png"
			style="padding-left: 15px; width: 170px; padding-top: 15px"
			alt="zen analytica Logo" />
		</a>

	</div>

	<div class="s">
		<ul class="mui-tabs__bar mui-tabs__bar--justified">
			<li><a data-mui-toggle="tab"
				data-mui-controls="pane-justified-1">source and target</a></li>
			<li><a data-mui-toggle="tab"
				data-mui-controls="pane-justified-2">set properties</a></li>
			<li class="mui--is-active"><a data-mui-toggle="tab"
				data-mui-controls="pane-justified-3">execute pipeline</a></li>
		</ul>


		<div class="mui-tabs__pane mui--is-active" id="pane-justified-3">

			<h1>Executed in Console</h1>
		</div>
	</div>
</body>
</html>