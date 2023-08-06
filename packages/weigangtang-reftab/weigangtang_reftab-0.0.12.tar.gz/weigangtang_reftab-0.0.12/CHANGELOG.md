# Change Log

* Version 0.0.5 (2021-07-20)
	* Intialize
	* Start from 0.0.5 as previous versions are all failed
	* Remove __os__, __re__, __string__ from 'install_requires', as they are built-in packages. Issue raise up if list those packages.

* Version 0.0.6 (2021-07-20)
	* Merge scripts into __init__.py. Script can not load function from another.

* Version 0.0.7 (2021-07-21)
	* Adjust the column width of reference table.

* Version 0.0.8 (2021-07-23)
	* Add `merge_duplicated_ref()`
		* merge keywords together
		* sort keywords by alphabet
	* When export to Excel
		* Assign references with no keyword to "No Category" sheet
		* Assign references with keyword of __" * "__ to "Important" sheet

* Version 0.0.9 (2021-08-02)
	* Add `check_ref_workbook()`
		* list sheets with missing columns
		* list references with incorrect format of authors and year
		* require `tabulate` package

* Version 0.0.10 (2021-08-03)
	* Add `clean_ref_workbook()`
		* correct column of 'Authors'
		* add 'Abbr' column on the basis of columns of 'Authors' and 'Year'
		* add 'Link' (as index) on the basis of columns of 'Abbr', 'Year', and 'Journal'
	* Change `auto_correct_author_string()`
		* instead of dealing with a list of author string, now it processes a single author string
			* split author by ';'
			* correct author one by one
		* its functionality move to `auto_correct_author_column()`
		* can automatically correct three cases:
			* extra space at the beginning of each author (segement)
			* extra space at the end of each author
			* single, isolated uppercase letter not followed with '.'
	* Add `auto_correct_author_column()`

* Version 0.0.11 (2021-08-08)
	* change print color in `get_pdf_list()`

* Version 0.0.12 (2021-09-12)
	* ensure code format follow PEP 8
	* set .git to track the entire package, rather than python script only
	* add .gitignore
