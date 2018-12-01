from wine import app

if __name__ == "__main__":
	app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
	app.run(debug=True, use_reloader=False)