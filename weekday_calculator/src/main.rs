use anyhow::Result;
use chrono::prelude::*;
use num_traits::FromPrimitive;
use std::io::{self, Write};

fn calculate_week_day(date: NaiveDate) -> String {
    // Get start day.
    let mut doomsday = match date.year() / 100 % 4 {
        0 => 2,
        1 => 0,
        2 => 5,
        3 => 3,
        _ => unreachable!("Modulo 4 failed, uh oh."),
    };

    doomsday += date.year() % 100 / 12;
    doomsday += date.year() % 100 % 12;
    doomsday += date.year() % 100 % 12 / 4;
    let doomsday = doomsday % 7;

    let mut start_day = match Month::from_u32(date.month())
        .expect("Chrono should ensure that this is always safe.")
    {
        Month::January => 3,
        Month::February => 28,
        Month::March => 14,
        Month::April => 4,
        Month::May => 9,
        Month::June => 6,
        Month::July => 11,
        Month::August => 8,
        Month::September => 5,
        Month::October => 10,
        Month::November => 7,
        Month::December => 12,
    };

    // Fix leap years.
    if date.year() % 4 == 0 && date.month() == 1 || date.month() == 2 {
        start_day += 1;
    }

    let difference_of_days = i32::try_from(date.day())
        .expect("Chrono should ensure that this is always safe.")
        - start_day;
    let day_of_week: i32 = doomsday + difference_of_days;

    match day_of_week.rem_euclid(7) {
        0 => String::from("Sunday"),
        1 => String::from("Monday"),
        2 => String::from("Tuesday"),
        3 => String::from("Wednesday"),
        4 => String::from("Thursday"),
        5 => String::from("Friday"),
        6 => String::from("Saturday"),
        _ => unreachable!("Modulo 7 failed, uh oh."),
    }
}

fn main() -> Result<()> {
    let date = loop {
        // First get the year.
        print!("Enter a year: ");
        io::stdout().flush()?;

        let mut year = String::new();
        io::stdin().read_line(&mut year)?;
        let year: i32 = match year.trim().parse() {
            Ok(y) => y,
            Err(e) => {
                println!("Error: {e}");
                continue;
            }
        };

        // Then get the month.
        print!("Enter a month: ");
        io::stdout().flush()?;

        let mut month = String::new();
        io::stdin().read_line(&mut month)?;
        let month = match month.trim().parse() {
            Ok(y) => y,
            Err(e) => {
                println!("Error: {e}");
                continue;
            }
        };

        if !(1..=12).contains(&month) {
            println!("Error: invalid month");
            continue;
        }

        // Then get the day.
        print!("Enter a day: ");
        io::stdout().flush()?;

        let mut day = String::new();
        io::stdin().read_line(&mut day)?;
        let day = match day.trim().parse() {
            Ok(y) => y,
            Err(e) => {
                println!("Error: {e}");
                continue;
            }
        };

        let date = NaiveDate::from_ymd_opt(year, month, day);

        match date {
            Some(d) => break d,
            None => {
                println!("Error: invalid date");
            }
        };
    };

    println!("{}", calculate_week_day(date));
    Ok(())
}
