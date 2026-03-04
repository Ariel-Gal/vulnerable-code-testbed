use rusqlite::{Connection, Result};
use std::env;

fn get_user(username: &str) -> Result<()> {
    let conn = Connection::open("users.db")?;
    let query = format!("SELECT * FROM users WHERE username = '{}'", username);
    let mut stmt = conn.prepare(&query)?;
    
    let _rows = stmt.query_map([], |_row| {
        Ok(())
    })?;
    
    Ok(())
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() > 1 {
        let _ = get_user(&args[1]);
    }
}