# 데이터베이스 연결 객체를 받아 테이블 이름 목록을 반환합니다.
def get_table_names(conn):
    """Return a list of table names."""
    table_names = []
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for table in tables.fetchall():
        table_names.append(table[0])
    return table_names

# 데이터베이스 연결 객체와 테이블 이름을 받아 해당 테이블의 컬럼 이름 목록을 반환합니다.
def get_column_names(conn, table_name):
    """Return a list of column names."""
    column_names = []
    columns = conn.execute(f"PRAGMA table_info('{table_name}');").fetchall()
    for col in columns:
        column_names.append(col[1])
    return column_names

# 데이터베이스 연결 객체를 받아 데이터베이스의 모든 테이블과 각 테이블의 컬럼 정보를 포함하는 사전 목록을 반환합니다.
def get_database_info(conn):
    """Return a list of dicts containing the table name and columns for each table in the database."""
    table_dicts = []
    for table_name in get_table_names(conn):
        columns_names = get_column_names(conn, table_name)
        table_dicts.append({"table_name": table_name, "column_names": columns_names})
    return table_dicts


def name_1(conn):
    # 데이터베이스 스키마 정보를 문자열로 변환하여 출력합니다.
    # Convert database schema information into a string for display.
    database_schema_string = "\n".join(
        [
            f"Table: {table['table_name']}\nColumns: {', '.join(table['column_names'])}"
            for table in get_database_info(conn)
        ]
    )
    return database_schema_string


# 데이터베이스에서 정보를 요청하고 결과를 처리하는 기능을 제공합니다.

def ask_database(conn, query):
    """Function to query SQLite database with a provided SQL query."""
    try:
        results = str(conn.execute(query).fetchall())
    except Exception as e:
        results = f"query failed with error: {e}"
    return results


def name_2():
    messages = [{
        "role":"user", 
        "content": "가장 많이 판매된 앨범은?"
    }]

    response = client.chat.completions.create(
        model='gpt-4o', 
        messages=messages, 
        tools= tools, 
        tool_choice="auto"
    )

    # Append the message to messages list
    response_message = response.choices[0].message 
    messages.append(response_message)

    return response_message


def name_3():
    # Step 2: determine if the response from the model includes a tool call.   
    tool_calls = response_message.tool_calls
    if tool_calls:
        # If true the model will return the name of the tool / function to call and the argument(s)  
        tool_call_id = tool_calls[0].id
        tool_function_name = tool_calls[0].function.name
        tool_query_string = eval(tool_calls[0].function.arguments)['query']
        
        # Step 3: Call the function and retrieve results. Append the results to the messages list.      
        if tool_function_name == 'ask_database':
            results = ask_database(conn, tool_query_string)
            
            messages.append({
                "role":"tool", 
                "tool_call_id":tool_call_id, 
                "name": tool_function_name, 
                "content":results
            })
            
            # Step 4: Invoke the chat completions API with the function response appended to the messages list
            # Note that messages with role 'tool' must be a response to a preceding message with 'tool_calls'
            model_response_with_function_call = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
            )  # get a new response from the model where it can see the function response
            print(model_response_with_function_call.choices[0].message.content)
        else: 
            print(f"Error: function {tool_function_name} does not exist")
    else: 
        # Model did not identify a function to call, result can be returned to the user 
        print(response_message.content) 


tools = [
    {
        "type": "function",
        "function": {
            "name": "ask_database",
            "description": "이 함수를 사용하여 사용자의 음악에 관한 질문에 답하세요. 입력은 완전히 형성된 SQL 쿼리여야 합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": f"""
                                사용자의 질문에 답하기 위해 정보를 추출하는 SQL 쿼리입니다.
                                SQL은 다음 데이터베이스 스키마를 사용하여 작성되어야 합니다:
                                {name_1()}
                                쿼리는 JSON이 아닌 일반 텍스트로 반환되어야 합니다.
                                """,
                    }
                },
                "required": ["query"],
            },
        }
    }
]