<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Zen_analytica</title>
<script src="js/mui.min.js"></script>
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
			<li class="mui--is-active"><a data-mui-toggle="tab"
				data-mui-controls="pane-justified-2">set properties</a></li>
			<li><a data-mui-toggle="tab"
				data-mui-controls="pane-justified-3">execute pipeline</a></li>
		</ul>



		<div class="mui-tabs__pane mui--is-active" id="pane-justified-2">
			<div class="mui-container">

				<form action="BlobToBlob" method="post" class="mui-form">
					<br> <br> <br>
					<div class="mui-textfield">
						<input type="text" name="path" id="path"> <label>Source
							File path</label>
					</div>
					<div class="mui-textfield">
						<input type="text" name="target_filepath" id="target_filepath">
						<label>Target File path</label>
					</div>
					<div class="mui-textfield">
						<input type="text" name="pipeline_name" id="pipeline_name">
						<label>Pipeline Name</label>
					</div>
					<div class="mui-textfield">
						<input type="text" name="act_name" id="act_name"> <label>Activity
							Name</label>
					</div>
					<div class="mui-textfield">
						<input type="text" name="activity_desc" id="activity_desc">
						<label>Activity Description</label>
					</div>

					<div class="mui-textfield">
						<input type="text" name="dataset_input" id="dataset_input">
						<label>DataSet Input</label>
					</div>
					<div class="mui-textfield">
						<input type="text" name="dataset_output" id="dataset_output">
						<label>DataSet Output</label>
					</div>
					<div class="mui-textfield">
						<input type="text" name="linkedserviceinput"
							id="linkedserviceinput"> <label>Input
							LinkedService Name</label>
					</div>
					<div class="mui-textfield">
						<input type="text" name="linkedserviceoutput"
							id="linkedserviceoutput"> <label>Output
							LinkedService Name</label>
					</div>
					<button type="submit" name="generate" id="generate" value="Execute"
						class="mui-btn mui-btn--raised">EXECUTE</button>

				</form>
			</div>
		</div>





	</div>
</body>
</html>