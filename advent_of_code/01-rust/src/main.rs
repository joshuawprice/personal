use std::fs::File;
use std::io::{BufReader, prelude::*};
use std::path::Path;

type Result<T, E = Box<dyn std::error::Error>> = std::result::Result<T, E>;


fn challenge_1() -> Result<i32> {
    let path = Path::new("input.txt");
    let file = File::open(&path)?;
    let reader = BufReader::new(file);

    let mut dial = 50;
    let mut count_of_zeroes = 0;
    for line in reader.lines() {
        let line = line?;
        let direction = &line[..1];
        let clicks = line[1..].parse::<i32>()?;

        if direction == "L" {
            dial = (dial - clicks) % 100;
        } else if direction == "R" {
            dial = (dial + clicks) % 100;
        }

        if dial == 0 {
            count_of_zeroes += 1;
        }
    }

    Ok(count_of_zeroes)
}

// The first method I used to solve challenge 2 (properly).
fn challenge_2_1() -> Result<i32> {
    
    let path = Path::new("input.txt");
    let file = File::open(&path)?;
    let reader = BufReader::new(file);

    let mut dial: i32 = 50;
    let mut count_of_zeroes = 0;
    for line in reader.lines() {
        let line = line?;
        let direction = &line[..1];
        let clicks = line[1..].parse::<i32>()?;

        if direction == "L" {
            dial -= clicks;
            count_of_zeroes += (dial - 1).div_euclid(100).abs();

            if dial + clicks == 0 {
                count_of_zeroes -= 1;
            }
        } else if direction == "R" {
            count_of_zeroes += (dial + clicks) / 100;
            dial += clicks;
        }
        dial = dial.rem_euclid(100);
    }

    Ok(count_of_zeroes)
}

// The second method I used to solve challenge 2. I like how this one's a little more elegant.
fn challenge_2_2() -> Result<i32> {
    let path = Path::new("input.txt");
    let file = File::open(&path)?;
    let reader = BufReader::new(file);

    let mut dial: i32 = 50;
    let mut count_of_zeroes = 0;
    for line in reader.lines() {
        let line = line?;
        let direction = &line[..1];
        let clicks = line[1..].parse::<i32>()?;

        if direction == "L" {
            count_of_zeroes += (clicks + (-dial).rem_euclid(100)) / 100;
            dial -= clicks;
        } else if direction == "R" {
            count_of_zeroes += (dial + clicks) / 100;
            dial += clicks;
        }
        dial = dial.rem_euclid(100);
    }

    Ok(count_of_zeroes)
}

// Challenge 2 wasn't cooperating for a while so I also brute forced it :/
fn challenge_2_3() -> Result<i32> {
    let path = Path::new("input.txt");
    let file = File::open(&path)?;
    let reader = BufReader::new(file);

    let mut dial = 50;
    let mut count_of_zeroes = 0;
    for line in reader.lines() {
        let line = line?;
        let direction = &line[..1];
        let clicks = line[1..].parse::<i32>()?;

        if direction == "L" {
            for _ in 0..clicks {
                dial -= 1;
                if dial == 0 {
                    count_of_zeroes += 1
                }
                if dial == -1 {
                    dial = 99
                }
            }
        } else if direction == "R" {
            for _ in 0..clicks {
                dial += 1;
                if dial == 100 {
                    count_of_zeroes += 1;
                    dial = 0;
                }
            }
        }
    }

    Ok(count_of_zeroes)
}

fn main() -> Result<()> {
    println!("Challenge 1: {}", challenge_1()?);
    println!("Challenge 2: {}", challenge_2_1()?);

    Ok(())
}
