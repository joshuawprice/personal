use std::fs::File;
use std::io::{self, BufReader, prelude::*};
use std::path::Path;

type Result<T, E = Box<dyn std::error::Error>> = std::result::Result<T, E>;

fn challenge_1() -> Result<i64> {
    let path = Path::new("input.txt");
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut invalid_ids_total = 0;

    for range in reader.split(b',') {
        let range = range?;

        // Each range should contain two numbers separated by a "-".
        let mut cursor = io::Cursor::new(range);
        let mut start_buf = vec![];
        let mut end_buf = vec![];

        cursor.read_until(b'-', &mut start_buf)?;
        start_buf.pop(); // Remove the '-'.
        cursor.read_until(b'-', &mut end_buf)?;

        let start = String::from_utf8(start_buf)?;
        let end = String::from_utf8(end_buf)?;

        for id in start.parse::<i64>()?..=end.parse()? {
            let i_as_bytes = id.to_string().into_bytes();
            let number_of_digits = i_as_bytes.len();

            // We only need to check even numbers.
            if number_of_digits % 2 != 0 {
                continue;
            }

            let first_half = &i_as_bytes[0..number_of_digits / 2];
            let last_half = &i_as_bytes[number_of_digits / 2..];

            if first_half == last_half {
                invalid_ids_total += id;
            }
        }
    }

    Ok(invalid_ids_total)
}

fn challenge_2() -> Result<i64> {
    let path = Path::new("input.txt");
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut invalid_ids_total: i64 = 0;

    for range in reader.split(b',') {
        let range = range?;
        let mut range = range.split(|b| b == &b'-');
        let start = String::from_utf8(range.next().unwrap().to_vec())?;
        let end = String::from_utf8(range.next().unwrap().to_vec())?;

        for id in start.parse::<i64>()?..=end.parse()? {
            let id_as_bytes = id.to_string().into_bytes();
            let number_of_digits = id_as_bytes.len();
            let factors = (1..=number_of_digits / 2).filter(|x| number_of_digits % x == 0);

            for factor in factors {
                let mut iter = id_as_bytes.chunks(factor);
                let is_invalid = iter.next().map_or(true, |first| iter.all(|x| x == first));
                if is_invalid {
                    invalid_ids_total += id;
                    break;
                }
            }
        }
    }

    Ok(invalid_ids_total)
}

fn main() -> Result<()> {
    println!("{}", challenge_1()?);
    println!("{}", challenge_2()?);
    Ok(())
}
