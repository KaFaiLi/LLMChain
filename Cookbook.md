**Power BI Cookbook: Data Import, Handling, and Manipulation (Comprehensive Edition)**

**Table of Contents**

1.  **Getting Started: The Power BI Interface**
    *   1.1  The Report View
    *   1.2  The Data View
    *   1.3  The Model View
    *   1.4  The Power Query Editor (Get & Transform Data)

2.  **Data Import: Connecting to Your Data**
    *   2.1  Common Data Sources (Excel, CSV, SQL Server, Web, etc.)
        *   2.1.1 Import vs. DirectQuery (Detailed Explanation)
        *   2.1.2 Specific Data Source Troubleshooting
    *   2.2  Connecting to a Folder (Importing Multiple Files)
        * 2.2.1 Handling different structures
    *   2.3  Connecting to a Database (SQL Server Example)
    *   2.4  Connecting to Web Data (API and Web Pages)
        * 2.4.1 API Pagination
    *   2.5  Connecting to other data sources (Sharepoint, etc.)
        * 2.5.1 SharePoint Specifics
    *   2.6 Combining multiple excel workbooks
        * 2.6.1 Different sheets in one workbook

3.  **Data Handling in Power Query Editor**
    *   3.1  The Power Query Interface
    *   3.2  Basic Data Transformations
        *   3.2.1  Choosing and Removing Columns
        *   3.2.2  Filtering Rows
            *   3.2.2.1 Advanced Filtering
        *   3.2.3  Data Type Conversion
            *   3.2.3.1 Locale Considerations
        *   3.2.4  Renaming Columns
        *   3.2.5  Replacing Values
        *   3.2.6  Splitting Columns
            * 3.2.6.1 Splitting by Multiple Delimiters
            * 3.2.6.2 Splitting by position
        *   3.2.7  Merging Columns
    *   3.3  Working with Dates and Times
        *   3.3.1  Extracting Date/Time Components
        *   3.3.2  Date/Time Calculations
    *   3.4  Handling Missing Values (Nulls)
        *   3.4.1  Replacing Nulls with Specific Values
        *   3.4.2  Filtering Out Rows with Nulls
    *   3.5  Working with Text Data
        *  3.5.1 Trim
        *  3.5.2 Clean
        *  3.5.3 Proper/Upper/Lower
        *  3.5.4 Combine Trim, Clean, Proper
    *   3.6  Grouping and Aggregating Data
        * 3.6.1 Group by multiple columns
    *   3.7  Pivoting and Unpivoting Columns
        * 3.7.1 Unpivoting multiple columns
    *   3.8  Appending Queries (Combining Tables Vertically)
    *   3.9  Merging Queries (Joining Tables Horizontally)
        * 3.9.1 Join kinds
        * 3.9.2 Fuzzy Matching

4.  **Advanced Data Manipulation**
    *   4.1  Custom Columns (M Language Basics)
        *   4.1.1  Creating Simple Calculations
        *   4.1.2  Using Conditional Logic (if-then-else)
            * 4.1.2.1 Nested ifs
        *   4.1.3  Working with Text Functions
        *   4.1.4  Working with Date Functions
        *   4.1.5 Using `let...in` for Clarity
        *   4.1.6 M Type System
    *   4.2  Parameters
        *   4.2.1  Creating Parameters
        *   4.2.2  Using Parameters in Queries
        * 4.2.3 Dynamic Data Sources
        * 4.2.4 User Input
        * 4.2.5 Parameter as filter value
        * 4.2.6 Parameter as a part of source file name
        * 4.2.7 Parameter between multiple queries
    *   4.3  Functions
        * 4.3.1 Creating Functions
        * 4.3.2 Input Limitation
        * 4.3.3 Recursive functions
    *   4.4  Error Handling
        * 4.4.1 Capturing Error Details
        * 4.4.2 Handling error on row level

5.  **Loading Data into the Power BI Model**
    *  5.1 Close and apply

6. **Additional Topics**
    * 6.1 Power Query vs. DAX
    * 6.2 Data Modeling Best Practices
        * 6.2.1 Star Schema
        * 6.2.2 Relationships
        * 6.2.3 Many-to-Many Relationships
    * 6.3 Query Folding
    * 6.4 Incremental Refresh
    * 6.5 Documentation
        * 6.5.1 Rename Steps
        * 6.5.2 Comments in M Code
        * 6.5.3 Description Property
    * 6.6 Deployment and Sharing
        * 6.6.1 Power BI Service
        * 6.6.2 Row-level security
        * 6.6.3 Data Refresh

**Detailed Chapters (Combined and Expanded)**

**1. Getting Started: The Power BI Interface**

*   **1.1 The Report View:**  Build visualizations (charts, tables, maps). Drag and drop fields from the data model.
*   **1.2 The Data View:** Tabular view of the data. Preview data, check data types, create simple calculated columns (DAX).
*   **1.3 The Model View:** Define relationships between tables (crucial for accurate reporting with multiple tables).
*   **1.4 The Power Query Editor (Get & Transform Data):**  Accessed via "Transform data."  Data cleaning, shaping, and transformation *before* loading into the model.

**2. Data Import: Connecting to Your Data**

*   **2.1 Common Data Sources:** ("Get data" on the Home ribbon)
    *   **Excel:**  (.xlsx, .xlsb, .xlsm).
    *   **Text/CSV:** (.csv and other delimited files).
    *   **SQL Server Database:**
    *   **Web:** (web pages and APIs).
    *   **Blank Query:** (for custom M code).
    *   **Many more...** (Azure, SharePoint, Salesforce, etc.)

    *   **2.1.1 Import vs. DirectQuery (Detailed Explanation):**
        *   **Import:**
            *   **Pros:**  Faster query performance (data cached). Wider range of Power Query/DAX.  Ideal for smaller datasets (under 1GB compressed is a good rule of thumb, but it can handle more).
            *   **Cons:** Data is a snapshot (needs refresh). Larger datasets = more memory/storage.
            *   **Best For:** Most common scenarios, especially complex transformations.
        *   **DirectQuery:**
            *   **Pros:** Data always up-to-date.  Good for very large datasets, real-time.
            *   **Cons:** Slower query performance (queries go to source). Limited Power Query/DAX. Increased source database load. Report design limitations.
            *   **Best For:** Real-time, very large datasets, data security at the source.
        *   **Switching Modes:** Possible, but switching *from* Import *to* DirectQuery might require simplification.
        *   **Data Size Limits (Import):** Practical limit depends on hardware (RAM) and model complexity.  Keep under 1GB (compressed) if possible. Premium offers higher limits.
        *   **DirectQuery Supported Sources:** SQL Server, Azure SQL Database, Azure Synapse, Oracle, Teradata, and others. Check documentation for the latest list.
        *   **DirectQuery Performance Impact:**  Queries go to your data source.  Optimize your database (indexes, views).

    *   **2.1.2 Specific Data Source Troubleshooting:**
        *   **General:** Check credentials, firewall, network, data source availability, permissions, and any necessary drivers.
        *   **API Specifics:**  Check authentication (API keys, OAuth), rate limits, and pagination.
            *   **Pagination Example (Conceptual M Code):**
                ```M
                // Function to fetch a single page
                let
                    GetPage = (pageNumber as number) =>
                    let
                        url = "https://api.example.com/data?page=" & Text.From(pageNumber),
                        source = Json.Document(Web.Contents(url)),
                        data = source[data]
                    in
                        data,

                    // Recursive function to fetch all pages
                    GetAllPages = (pageNumber as number, previousData as list) =>
                    let
                        currentPage = GetPage(pageNumber),
                        newData = previousData & currentPage,
                        hasMorePages = List.Count(currentPage) > 0, //Example
                        result = if hasMorePages then GetAllPages(pageNumber + 1, newData) else newData
                    in
                        result,
                    finalResult = GetAllPages(1, {})
                in
                    finalResult
                ```

    *   **Example: Connecting to an Excel File:** "Get data" -> "Excel" -> select file -> choose sheet(s)/table(s) -> "Transform Data".

*   **2.2 Connecting to a Folder (Importing Multiple Files):**
    *   Powerful for combining files with the *same structure*.  "Get data" -> "Folder" -> browse to folder -> "Transform Data" -> "Combine Files" (double down arrow).
    * **2.2.1 Handling different structures:**
        * Aim for consistent structures. If slightly different structures, use custom function with conditional logic (`if [ColumnName] = null then ... else ...`) or `Table.RenameColumns`.
         *   **Example (Combining Files with Different Column Names):**
            ```M
            let
                Source = Folder.Files("C:\YourFolderPath"),
                ProcessFile = (file as binary) =>
                let
                    workbook = Excel.Workbook(file),
                    sheet = workbook{[Item="Sheet1",Kind="Sheet"]}[Data],
                    renamed = Table.RenameColumns(sheet, {
                        {"OldColumnName1", "StandardColumnName1"},
                        {"OldColumnName2", "StandardColumnName2"}
                    }),
                   typed = Table.TransformColumnTypes(renamed, {
                       {"StandardColumnName1", type text},
                       {"StandardColumnName2", type number}
                   })

                in
                    typed,
                transformed = Table.AddColumn(Source, "Processed", each ProcessFile([Content])),
                removed = Table.RemoveColumns(transformed,{"Content"}),
                expanded = Table.ExpandTableColumn(removed, "Processed", {"StandardColumnName1", "StandardColumnName2"})
            in
                expanded
            ```
    * Combining Different File Type is generally NOT recommended.

*   **2.3 Connecting to a Database (SQL Server Example):** "Get data" -> "SQL Server database" -> server/database name -> "Import" or "DirectQuery" -> credentials -> choose tables/views -> "Transform Data".

*   **2.4 Connecting to Web Data:**
    *   **Web Pages:** "Get data" -> "Web" -> URL.  Works best for well-structured HTML tables.
    *   **Web APIs:** "Get data" -> "Web" -> API endpoint URL.  May need API keys.  Often returns JSON/XML; use `Json.Document` or `Xml.Document` to parse.
    * **2.4.1 API Pagination:** Covered in section 2.1.2

*   **2.5 Connecting to other data sources:** Follow prompts, provide credentials.

    *   **2.5.1 SharePoint Specifics:**
        1.  Get Data -> SharePoint Folder/SharePoint Online List.
        2.  Enter the *site* URL.
        3.  Choose authentication (Microsoft/Organizational account).
        4.  Navigate to list/library.

*   **2.6 Combining multiple excel workbooks:** Use "Folder" connector (2.2). Ensure same structure.
    * **2.6.1 Different sheets in one workbook:**
        * Import different sheets individually.
        * Ensure each sheet has correct header.

**3. Data Handling in Power Query Editor**

*   **3.1 The Power Query Interface:**
    *   **Query Settings Pane:** "Applied Steps" (each transformation is a step).  Click a step to see data at that point. Rename, delete, reorder steps.
    *   **Formula Bar:** Shows M code. Edit directly (advanced). (View -> Formula Bar).
    *   **Data Preview:** Shows data after transformations.
    *   **Ribbon:** Transformation tools (Home, Transform, Add Column, View).

*   **3.2 Basic Data Transformations:**

    *   **3.2.1 Choosing and Removing Columns:**
        *   **Choose Columns:** (Home -> "Choose Columns"). Select columns to *keep*. More resilient to changes.
        *   **Remove Columns:** Select column(s) -> right-click -> "Remove Columns".

    *   **3.2.2 Filtering Rows:** Filter dropdown arrow in column header.
        *   **3.2.2.1 Advanced Filtering:** Combine conditions (AND/OR). "Custom Filter".

    *   **3.2.3 Data Type Conversion:** Click data type icon (column header). Choose correct type.
        *   **3.2.3.1 Locale Considerations:** Use "Using Locale..." for correct interpretation of text-to-number/date conversions.

    *   **3.2.4 Renaming Columns:** Double-click header, or right-click -> "Rename".

    *   **3.2.5 Replacing Values:** Right-click on a value -> "Replace Values". Useful for errors, standardization, nulls (3.4).

    *   **3.2.6 Splitting Columns:** (Home -> "Split Column"). By Delimiter, Number of Characters, Positions, Lowercase to Uppercase.
        *   **3.2.6.1 Splitting by Multiple Delimiters:** Use M code:
            ```M
            Table.SplitColumn(Source, "ColumnName", Splitter.SplitTextByAnyDelimiter({",", ";"}), {"Column1", "Column2"})
            ```
        * **3.2.6.2 Splitting by position:** e.g. `{0, 5, 12}`

    *   **3.2.7 Merging Columns:** Select columns (Ctrl+click) -> (Home -> "Merge Columns"). Choose separator, new column name.

*   **3.3 Working with Dates and Times:**

    *   **3.3.1 Extracting Date/Time Components:** (Add Column -> "Date" or "Time"). Extract Year, Month, Day, Quarter, Week, Hour, Minute, etc.

    *   **3.3.2 Date/Time Calculations:** Create custom columns (4.1).

*   **3.4 Handling Missing Values (Nulls):**

    *   **3.4.1 Replacing Nulls with Specific Values:** Select column -> (Transform -> "Replace Values").  "Value To Find": blank (or `null`).  "Replace With": your value.

    *   **3.4.2 Filtering Out Rows with Nulls:** Filter dropdown -> uncheck "null".

*   **3.5 Working with Text Data:**
    * **3.5.1 Trim:** Transform > Format > Trim.
    * **3.5.2 Clean:** Transform > Format > Clean.
    * **3.5.3 Proper/Upper/Lower:** Transform > Format > select case.
    * **3.5.4 Combine Trim, Clean, Proper:** Apply all three in sequence.

*   **3.6 Grouping and Aggregating Data:** (Home -> "Group By"). Choose column(s) to group by. Define new columns (aggregations): Operation (Sum, Average, etc.), Column, New column name.
    * **3.6.1 Group by multiple columns:** Select multiple columns in Group By dialog.

*   **3.7 Pivoting and Unpivoting Columns:**

    *   **Pivoting:** Rows to columns (summary tables). Select column for new headers -> (Transform -> "Pivot Column").
    *   **Unpivoting:** Columns to rows (normalization). Select columns to *keep* -> right-click -> "Unpivot Other Columns".
        * **3.7.1 Unpivoting multiple columns:** Covered in 3.7

*   **3.8 Appending Queries:** Combines rows from tables with *same structure* (vertically). (Home -> "Append Queries").

*   **3.9 Merging Queries:** Combines columns from two tables based on common column (horizontal join). (Home -> "Merge Queries").
    *   **3.9.1 Join Kinds (Use Visuals):**
        *   **Left Outer:** All from left, matching from right.
        *   **Right Outer:** All from right, matching from left.
        *   **Full Outer:** All from both.
        *   **Inner:** Only matching rows.
        *   **Left Anti:** Rows from left that *don't* match right.
        *   **Right Anti:** Rows from right that *don't* match left.
    *   **3.9.2 Fuzzy Matching:** Use for inexact matches.

**4. Advanced Data Manipulation**

*   **4.1 Custom Columns (M):** (Add Column -> "Custom Column").
    *   **4.1.1 Simple Calculations:** `[Quantity] * [Unit Price]`
    *   **4.1.2 Conditional Logic:** `if [Sales] > 1000 then "High" else "Low"`
        * **4.1.2.1 Nested ifs:**
            ```M
            if [Country] = "USA" then
                if [State] = "CA" then "California"
                else "Other US State"
            else if [Country] = "Canada" then "Canada"
            else "Other Country"
            ```
    *   **4.1.3 Text Functions:**
        ```M
        Text.Start([FullName], Text.PositionOf([FullName], " "))  // Extract first name
        Text.Upper([ColumnName])
        Text.Middle([ProductCode], 3, 5)
        ```
    *   **4.1.4 Date Functions:**
        ```M
        Duration.Days([EndDate] - [StartDate])
        Date.AddDays([OrderDate], 30)
        Date.Year([OrderDate])
        Date.MonthName([OrderDate])
        ```
    *   **4.1.5 Using `let...in`:**
        ```M
        let
            UnitPrice = [Price] / [Quantity],
            Discount = if UnitPrice > 100 then 0.1 else 0.05,
            FinalPrice = UnitPrice * (1 - Discount)
        in
            FinalPrice
        ```
    * **4.1.6 M Type System:**  text, number, date, time, datetime, logical, list, record, table, function, any, none.  `as type`.

*   **4.2 Parameters:** Make queries dynamic.
    *   **4.2.1 Creating Parameters:** (Home -> Manage Parameters -> New Parameter).  Name, description, type, default/allowed values.
    *   **4.2.2 Using Parameters:** Refer to parameter by name in M code: `Table.SelectRows(Source, each [OrderDate] >= StartDate)`
    * **4.2.3 Dynamic Data Sources:** Use parameters for file paths, server names, URLs.
    * **4.2.4 User Input:** In report, "Transform data" -> "Edit Parameters".
    * **4.2.5 Parameter as filter value:** `Table.SelectRows(Source, each [ColumnName] = FilterValue)`
    * **4.2.6 Parameter as a part of source file name:**
       ```M
        let
            YearParam = Text.From(YearParameter),
            Source = Excel.Workbook(File.Contents("C:\Data\Sales_" & YearParam & ".xlsx"), null, true)
        in
            Source
        ```
    * **4.2.7 Parameter between multiple queries:** Possible.

*   **4.3 Functions:** Reusable code blocks.
    * **4.3.1 Creating functions:**
        ```M
        (parameter1 as type, parameter2 as type, ...) =>
        let
            // Transformation steps
            result = ...
        in
            result
        ```
        *Example:*
        ```M
        (email as text) =>
        let
            atPosition = Text.PositionOf(email, "@"),
            domain = Text.Range(email, atPosition + 1, Text.Length(email) - atPosition - 1)
        in
            domain
        ```
        *Invoking:* Add Column -> Invoke Custom Function.
     *   **Practical Example (Phone Number Cleaning):**
        ```M
        (phoneNumber as text) =>
        let
            cleaned = Text.Remove(phoneNumber, {"(", ")", "-", " ", "."}),
            formatted = if Text.Length(cleaned) = 10 then "+1" & cleaned else cleaned
        in
            formatted
        ```
    * **4.3.2 Input Limitation:**  Define types clearly.
    * **4.3.3 Recursive functions:**  Essential for hierarchical data/API pagination. (See 2.1.2)

*   **4.4 Error Handling:** `try ... otherwise`.
    *   **4.4.1 Capturing Error Details:**
        ```M
        Table.AddColumn(Source, "PriceWithErrors", each
          try [UnitPrice] * [Quantity]
          otherwise [ErrorMessage = "Calculation Failed", ErrorDetails = "Check UnitPrice and Quantity"]
        )
        ```
    * **4.4.2 Handling error on row level:**
        ```M
          Table.AddColumn(Source, "Price Calculation", each
              try
                  if [Quantity] = 0 then error "Quantity cannot be zero"
                  else [UnitPrice] * [Quantity]
              otherwise null
          )
        ```

**5. Loading Data into the Power BI Model**

*   **5.1 Close & Apply:** Loads transformed data into model.

**6. Additional Topics**

*   **6.1 Power Query vs. DAX:**
    *   **Power Query:** Data *shaping* and *cleaning*.
    *   **DAX:** *Aggregation* and calculations dependent on report context.
    *   **Performance:** Power Query transformations generally more efficient for cleaning/shaping.
*   **6.2 Data Modeling Best Practices:**
    *   **6.2.1 Star Schema:** Fact tables and dimension tables. Recommended.
    *   **6.2.2 Relationships:** Crucial for accuracy. Define correctly.
    *   **6.2.3 Many-to-Many Relationships:** Use a bridge table.

*   **6.3 Query Folding:** Power Query translates transformations to native data source queries (e.g., SQL).
    *   **Benefits:** Improves performance.
    *   **Check:** Right-click step -> "View Native Query" (enabled = folding).
    *   **Prevent Folding:** Complex M code, certain connectors.
    *   **Best Practices:** Keep transformations simple. Test for folding.

*   **6.4 Incremental Refresh:**  Set up in Power BI Service (Premium/PPU).  Define RangeStart/RangeEnd parameters.

*   **6.5 Documentation:**
    *   **6.5.1 Rename Steps:** Descriptive names.
    *   **6.5.2 Comments in M Code:** `//` (single-line) and `/* ... */` (multi-line).
    *   **6.5.3 Description Property:** Add descriptions to queries/columns.

* **6.6 Deployment and Sharing**
    * **6.6.1 Power BI Service:** Publish your report.
    * **6.6.2 Row-level security:** Restrict data access by user roles.
    * **6.6.3 Data Refresh:** Scheduled/on-demand refresh in Power BI Service.
Okay, let's significantly enhance the Data Modeling section, adding even more detail, advanced concepts, and practical considerations. We'll cover more nuanced aspects of relationships, explore different modeling techniques, and delve deeper into best practices.

**6. Data Modeling in Power BI: The Model View (Comprehensive Edition)**

**(This expanded section replaces the previous Section 6)**

**6. Data Modeling in Power BI: The Model View**

After loading your transformed data, the Model View is where you forge the relationships between tables, establishing the *semantic model* that underpins your entire Power BI report. This is more than just connecting boxes; it's about creating a clear, efficient, and understandable representation of your data's meaning. A well-designed model is the single biggest factor in report performance, accuracy, and maintainability.

**6.1  Understanding Relationships: A Deeper Dive**

*   **What are Relationships?** Relationships are logical connections between tables based on shared columns (keys). They *do not* physically combine the data; instead, they define how Power BI should interpret the connections between rows in different tables.

*   **Why are they Essential?** (Expanded)
    *   **Filtering Across Tables (Context Propagation):** Relationships define how *filter context* flows between tables. When you select a value in a visualization (e.g., a specific year in a slicer), that selection acts as a filter. Relationships determine how that filter affects other related tables. This is the cornerstone of interactive analysis.
    *   **Accurate Calculations (DAX Context):** DAX measures (calculations) rely on relationships to correctly aggregate and contextualize data. Without relationships, DAX would have no way to know how to relate sales figures to products, customers, or time periods.
    *   **Drill-Through and Drill-Down:** Relationships enable users to seamlessly navigate from summary-level data to more granular details.
    *   **Data Integrity:** Relationships help enforce data integrity (to a degree) by ensuring that only related data is combined.

*   **Key Concepts (Detailed):**
    *   **Primary Key:** Uniquely identifies each row in a table. Must be unique and non-null.  Ideally, it should also be:
        *   **Immutable:**  The value should never change.
        *   **Meaningless:**  It should not have any business meaning (e.g., don't use a Social Security Number as a primary key).  Surrogate keys (auto-incrementing numbers) are often preferred.
        * **Data Type:** Often Integer type.
    *   **Foreign Key:** References the primary key of another table.  Establishes the link.  Foreign keys *can* contain null values (depending on the relationship's requirements), but this impacts how the relationship behaves.
    *   **Cardinality (Detailed):**
        *   **One-to-Many (1:*):** The most common and desirable relationship.  A single row in the "one" side table (typically a dimension table) can relate to zero, one, or many rows in the "many" side table (typically a fact table).  *Example:*  A `Customer` can have many `Orders`. *Filters propagate from the 'one' side to the 'many' side by default.*
        *   **Many-to-One (*:1):**  Just the reverse perspective of a one-to-many relationship.
        *   **One-to-One (1:1):**  Rare.  Often indicates that the data could be combined into a single table.  Sometimes used for:
            *   **Security:** Separating sensitive data into a separate table with restricted access.
            *   **Performance:**  Splitting a very wide table into smaller tables (but be cautious; this can sometimes *decrease* performance if not done carefully).
            *   **Large Text/Binary Data:**  Storing large text or binary data (images, documents) in a separate table to improve performance of queries that don't need that data.
        *   **Many-to-Many (*:*):**  *Avoid direct many-to-many relationships whenever possible.* They introduce ambiguity and can significantly impact performance and the accuracy of calculations.
            *   **Ambiguity:**  When filtering, it's not always clear which path Power BI should take to relate the data.
            *   **Performance:**  Power BI has to perform complex internal joins to resolve many-to-many relationships.
            *   **DAX Complexity:**  DAX calculations involving many-to-many relationships can be more complex to write and understand.
            *   **Bridge Table Solution (Essential):**  The standard and recommended solution is to create a **bridge table** (also known as a junction table or linking table). The bridge table contains the unique combinations of keys from the two many-to-many tables, effectively breaking the many-to-many relationship into two one-to-many relationships.
              *Example (Product and Promotion):*
                * `Product`: `ProductID` (PK), `ProductName`
                * `Promotion`: `PromotionID` (PK), `PromotionName`
                * *Direct Many-to-many:* A product can be part of many promotions and a promotion can have many products.
                * *Bridge Table Solution:*
                    * `ProductPromotion`: `ProductID` (FK to `Product`), `PromotionID` (FK to `Promotion`) -- These two columns together form the composite primary key of this table.
                    * Now you have: `Product` (1) -- (*) `ProductPromotion` and `Promotion` (1) -- (*) `ProductPromotion`.

    *   **Cross-Filter Direction (Critical):**
        *   **Single:**  Filters flow in one direction: from the "one" side to the "many" side of a one-to-many relationship. This is the *default and most common* setting.  It's the most efficient and predictable.
        *   **Both:**  Filters flow in *both* directions.  *Use with extreme caution!*
            *   **When to Consider "Both":**
                *   **Many-to-Many Relationships (without a bridge table – not recommended):** If you *must* use a direct many-to-many relationship, you'll likely need to set the cross-filter direction to "Both."
                *   **Dimension-on-Dimension Filtering:**  If you need to filter one dimension table based on selections in another dimension table, and there's no direct relationship between them, you *might* need to use "Both" on the relationships connecting them to a common fact table. *However*, it's often better to redesign your model to avoid this.
                *   **Certain Advanced DAX Calculations:** Some complex DAX calculations might require bidirectional filtering, but this is relatively rare.
            *   **Problems with "Both":**
                *   **Ambiguity:** Can lead to unexpected filtering behavior, especially in complex models.
                *   **Performance:** Can significantly degrade performance, especially with large tables.
                *   **Circular Dependencies:** Can create circular dependencies, where filters loop endlessly between tables, causing errors.

    *   **Active vs. Inactive Relationships:**
        *   You can have *multiple* relationships between two tables, but only *one* can be active at a time.
        *   **Active Relationship:**  Used by default for filtering and calculations.  Represented by a solid line in the Model View.
        *   **Inactive Relationship:**  Not used by default.  Represented by a dashed line.
        *   **Why Inactive Relationships?**  Often used for **role-playing dimensions**.
            *   **Role-Playing Dimensions:**  A single dimension table that plays multiple roles in relation to a fact table. *Example:* A `Date` table can be related to a `Sales` table multiple times:
                *   `OrderDate` (Active relationship)
                *   `ShipDate` (Inactive relationship)
                *   `DueDate` (Inactive relationship)
            *   To use an inactive relationship in a DAX calculation, you use the `USERELATIONSHIP` function. *Example:*
                ```DAX
                Total Shipped Sales = CALCULATE(
                    SUM(Sales[SalesAmount]),
                    USERELATIONSHIP(Sales[ShipDateKey], Dates[DateKey])
                )
                ```

**6.2  Working in the Model View (Practical Techniques)**

*   **The Interface (Detailed):**
    *   **Layout:**  Organize your tables logically.  Place related tables close to each other.  Use a consistent layout (e.g., dimensions above facts, or dimensions to the left of facts).
    *   **Zoom:** Use the zoom controls to adjust the view.
    * **Multiple Layouts:** You can have multiple diagram layouts to organize complex data model.
    * **Focus Mode:** Click a table, and click the focus mode icon in the bottom, this will show only the selected table and the related table.

*   **Creating Relationships:**
     *   **Drag and Drop:** The most intuitive method, Power BI will try to guess settings, but always *verify*.
    *   **Manage Relationships Dialog:** For precise control.
    * **Create relationship in diagram view:** right click and create relationship.

*   **Editing and Deleting:**  Double-click (edit) or right-click (delete) relationship lines.

*   **Auto-Detect:**  Generally, *disable* auto-detect after the initial import.  It's better to create relationships manually for accuracy and control.  (File -> Options and settings -> Options -> Current File -> Data Load -> Uncheck "Autodetect new relationships after data is loaded").

* **Hiding Columns and Tables:**
  * Right-click on the field/table to Hide. This will hide it from Report view, but not Data View.
  * In the property pane, set `IsHidden` to True. This will hide it from all views.

* **Table properties:**
    * **Name:** Table name
    * **Description:** Describe the meaning and usage.
    * **Synonyms:** Alternative names for table to be used in Q&A.
    * **IsHidden:** Hide the table
    * **Row Label:** Defines the default row label
    * **Key Columns:** Set which columns should be treated as key.
    * **Storage mode:** Import/DirectQuery/Dual. Dual = both Import and DirectQuery.
    * **Feature Table:** Promote the table to be reused in other reports.

* **Column properties:**
    * **Name:** Column name
    * **Description:** Describe the meaning and usage.
    * **Synonyms:** Alternative names for Q&A feature.
    * **Data type:**  Ensure correct data types (critical for calculations).
    * **Format:**  Control how the data is displayed (e.g., date format, number of decimal places).
    * **IsHidden:** Hide from report.
    * **Summarize by:** Default aggregation (Sum, Average, Count, etc.).  This is what happens if you drag the column directly onto a visual.
    * **Sort by column:**  Control how the column is sorted.  *Crucially*, you can use this to sort a text column (e.g., "MonthName") by a related numerical column (e.g., "MonthNumber").  This is essential for correct chronological sorting.
    * **Data Category:**  Specify what the data represents (e.g., Address, City, Country, Latitude, Longitude, URL, Image URL). This helps Power BI understand the data's semantics and enables features like map visualizations.

* **Hierarchies:**
  *  Create a hierarchy by dragging column into another one. This creates a drill-down path in report. (e.g. Year -> Quarter -> Month -> Day). Right click and create.
  * Give descriptive names to the hierarchies.

**6.3  Advanced Data Modeling Techniques**

*   **Snowflake Schema:**
    *   Dimension tables are *normalized* (broken down into multiple related tables). *Example:*  Instead of a single `Product` table, you might have `Product`, `ProductSubcategory`, and `ProductCategory` tables.
    *   **Pros:** Can reduce data redundancy (if dimensions have many attributes that are shared).
    *   **Cons:**  More complex queries, can negatively impact performance in Power BI.  Generally *not recommended* for Power BI; a star schema is usually preferred.
* **Calculated Tables:**
    * Create table with DAX expressions. Useful for creating:
        *   Date tables
        *   Bridge tables
        *   Tables for advanced calculations
* **Disconnected Tables:**
    * Tables that are *not* directly related to any other tables in the model.
    * **Uses:**
        *   **Parameter Tables:**  For "What-If" analysis.  Create a table with a single column containing a range of values (e.g., discount percentages).  Then, use a DAX measure to apply the selected value from this table to your calculations.
        *   **Slicers without Filtering:**  Create a disconnected table with values you want to use in a slicer, but you *don't* want the slicer to filter the main data model.  You then use DAX to control how the selection in the slicer affects your calculations.
* **Composite Models:**
    * Combine data from multiple sources using different storage modes (Import, DirectQuery, Dual) in the same model.
    * Useful for combining large datasets (DirectQuery) with smaller, more frequently used datasets (Import).
* **Aggregation Tables:**
    * Pre-calculated summary tables that store aggregated data at a higher level of granularity (e.g., daily sales totals instead of individual transactions).
    * Can significantly improve performance for reports that primarily show aggregated data.
    * Can be combined with detailed tables in a composite model.
    * Power BI can automatically use aggregation tables if they are properly configured.

**6.4 Data Modeling Best Practices (Extended)**

*   **Star Schema (Prioritize):**  Aim for a star schema whenever possible. It's the most efficient and understandable design for Power BI.
*   **Bridge Tables for Many-to-Many:**  *Always* use bridge tables to resolve many-to-many relationships.
*   **Consistent Naming Conventions:**  Essential for maintainability and collaboration.
*   **Hide Foreign Key Columns:** Hide foreign key columns from the Report View (in the fact table).
*   **Date Table (Essential):**
    *   Create a dedicated date table.
    *   Mark it as a date table.
    *   Include all relevant date/time attributes.
    *   Link it to your fact tables using the appropriate date columns.
*   **Consistent Data Model:**  Promote consistency across reports.
*   **Documentation:**
    *   Use table and column descriptions.
    *   Rename "Applied Steps" in Power Query.
    *   Add comments to your M code and DAX.
*   **Performance Tuning:**
    *   **Minimize Data Volume:** Import only the data you need.
    *   **Use Appropriate Data Types:**  Smaller data types (e.g., `Int` instead of `BigInt` if possible) can improve performance.
    *   **Avoid Bidirectional Filtering:** Use it only when absolutely necessary.
    *   **Optimize DAX:** Write efficient DAX measures.
    *   **Consider Aggregation Tables:** For large datasets and reports that focus on aggregated data.
* **Avoid Circular Dependencies:** If you see the warning about circular dependencies, review your relationships and cross filter direction.
*   **Keep It Simple:**  Start with a simple model and add complexity only when needed.  A simpler model is easier to understand, maintain, and debug.
* **Test Thoroughly:** Always verify that your relationships and calculations are producing the correct results.
