Perfeito, Gabriel! Aqui está o **README completo em inglês**, já todo formatado em **uma única seção de Markdown** pronta para copiar e colar:

````markdown
# Virtual Car Agent

**Note:** Temporary repository

An interactive virtual assistant developed in Python to help users find cars based on filters such as make, model, year, fuel type, transmission, price, and more. The agent chats with the user, searches a database via the MCP protocol, and returns results in a clear and user-friendly format.

---

## Project Structure

Tech-Challege-C2S/
│
├─ agent.py               # Main assistant code
├─ carros.csv             # Sample vehicle data
├─ inventario.db          # SQLite database (not versioned)
├─ models.py              # Database models
├─ popular_bd.py          # Script to populate the database
├─ requirements.txt       # Project dependencies
├─ README.md              # Project documentation
├─ venv/                  # Virtual environment (not versioned)
└─ mcp/                   # MCP protocol module
   ├─ __init__.py         # Package initializer
   ├─ client.py           # MCP client
   ├─ server.py           # MCP server
   ├─ message_type.py     # Protocol message types
   └─ protocol.py         # MCP protocol logic

---

## Installation & Setup

1. **Clone this repository:**

```bash
git clone https://github.com/gabriellemosc/C2S---Challenge.git
cd C2S---Challenge
````

2. **Create and activate a virtual environment (optional but recommended):**

```bash
python3 -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

3. **Install the dependencies:**

```bash
pip install -r requirements.txt
```

4. **Start the MCP server in a separate terminal:**

```bash
python3 -m mcp.server
```

---

## How to Use

1. **Run the agent in a new terminal (keep the server running):**

```bash
python3 agent.py
```

2. **Follow the assistant instructions:**

   * Enter the car’s make, model, year, fuel type, and price range.
   * The agent will query the database via MCP and display the results.
   * You can choose to perform a new search or exit at the end.

3. **Example Interaction:**

```
👋 Hello! I'm Gabriel, your virtual assistant to find your car.
Let's talk about what you're looking for...

Ok! Which car make are you interested in? Toyota, Honda, Volkswagen, etc...
> Toyota

And within Toyota, do you have a preferred model?
> Corolla

What about the year? Any specific range?
> 2018-2022

...
🔎 Alright, let me check what we have.
This might take a moment...

✅ I found 3 cars that might interest you:
1. 🟢 Toyota Corolla (2019)
     Black | 📊 35,000 km
     ⚙️ Transmission: Automatic | ⛽ Fuel: Flex
     💰 $95,000.00
     ✅ Available for test drive!

🔁 Do you want to make a new search? (y/n):
```

---

## Populating the Database

If you want to generate sample data:

```bash
python3 popular_bd.py
```

This script will populate the SQLite database (`inventario.db`) with random vehicles for testing purposes.

---

## MCP Protocol

* The MCP module handles communication between the agent and the database server.
* **Server:** `mcp.server`
* **Client:** `mcp.client`
* **Protocol logic:** `mcp.protocol`
* **Message types:** `mcp.message_type`

Make sure the **server is running** before starting the agent.

---

## Contact

**Gabriel Lemos**

* GitHub: [https://github.com/gabriellemosc](https://github.com/gabriellemosc)

