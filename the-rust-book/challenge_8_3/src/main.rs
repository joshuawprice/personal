use std::collections::HashMap;
use std::io;

enum Inputs {
    Input(String),
    List(Option<String>),
    Quit,
}

fn read_input() -> Inputs {
    let mut input = String::new();
    io::stdin()
        .read_line(&mut input)
        .expect("Failed to read line.");

    input = input.trim().into();

    if input.starts_with("ls") {
        if input.chars().count() > 3 {
            return Inputs::List(Some(input[2..].trim().to_string()));
        }
        return Inputs::List(None);
    }

    if input.starts_with("q") {
        return Inputs::Quit;
    }

    Inputs::Input(input)
}

fn main() {
    println!("Add people to departments. At any time type \"ls [department]\" to list additions.");
    let mut company: HashMap<String, Vec<String>> = HashMap::new();

    loop {
        println!("Enter a department.");
        let department = match read_input() {
            Inputs::Input(input) => input,
            Inputs::List(requested_department) => {
                if let Some(department) = requested_department {
                    if let Some(employees) = company.get_mut(&department) {
                        employees.sort();
                        println!("{:?}", &employees)
                    } else {
                        println!("Department doesn't exist.");
                        continue;
                    }
                } else {
                    println!("{:?}", &company);
                }
                continue;
            }
            Inputs::Quit => break,
        };

        println!("Enter an employee name.");
        let employee_name = match read_input() {
            Inputs::Input(input) => input,
            Inputs::List(requested_department) => {
                if let Some(department) = requested_department {
                    if let Some(employees) = company.get_mut(&department) {
                        employees.sort();
                        println!("{:?}", &employees)
                    } else {
                        println!("Department doesn't exist.");
                        continue;
                    }
                } else {
                    println!("{:?}", &company);
                }
                continue;
            }
            Inputs::Quit => break,
        };

        // Add department to hashmap if needed, then add employee to department.
        company.entry(department).or_default().push(employee_name);
    }
}
