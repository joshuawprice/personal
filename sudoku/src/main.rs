use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::time::{Duration, Instant};


const BOARD_SIZE: usize = 9;


fn check_row_vec(board: [[u32; BOARD_SIZE]; BOARD_SIZE], row: usize) -> Vec<u32> {
    /*
    Generates a vector of non zero numbers present within a given row
    */
    let mut numbers_present: Vec<u32> = vec![];

    for c in 0..board.len() {
        if board[c][row] != 0 {
            numbers_present.push(board[c][row]);
        }
    }

    return numbers_present;
}


fn check_row(board: [[u32; BOARD_SIZE]; BOARD_SIZE], row: usize, num: u32) -> bool {
    /*
    Function to check if a row has num present, returns false if so
     */
    for c in 0..board.len() {
        if board[c][row] == num {
            return false;
        }
    }

    return true;
}


fn check_col_vec(board: [[u32; BOARD_SIZE]; BOARD_SIZE], col: usize) -> Vec<u32> {
    /*
    Generate vector of used numbers for a column
     */
    let mut numbers_present: Vec<u32> = board[col].to_vec();
    numbers_present.retain(|&n| n != 0);

    return numbers_present;
}


fn check_col(board: [[u32; BOARD_SIZE]; BOARD_SIZE], col: usize, num: u32) -> bool {
    /*
    Function to check if num is present in a column
     */
    for r in 0..board[col].len() {
        if board[col][r] == num {
            return false;
        }
    }

    return true;
}


fn check_box_vec(board: [[u32; BOARD_SIZE]; BOARD_SIZE], col: usize, row: usize) -> Vec<u32> {
    /*
    Function to generate vector of non-zero numbers present in a box
     */
    let mut numbers_present: Vec<u32> = vec![];

    let start_col: usize = (col / 3) * 3;
    let start_row: usize = (row / 3) * 3;
    const BOX_SIZE: usize = BOARD_SIZE / 3;

    for c in 0..BOX_SIZE {
        for r in 0..BOX_SIZE {
            if board[start_col + c][start_row + r] != 0 {
                numbers_present.push(board[start_col + c][start_row + r]);
            }
        }
    }

    return numbers_present;
}


fn check_box(board: [[u32; BOARD_SIZE]; BOARD_SIZE], col: usize, row: usize, num: u32) -> bool {
    /*
    Checks every position within 3x3 box corresponding to current column and row and returns false is num is found
     */
    const SQUARE_WIDTH: usize = BOARD_SIZE / 3;
    let box_col: usize = (col / 3) * 3;
    let box_row: usize = (row / 3) * 3;

    for c in 0..SQUARE_WIDTH {
        for r in 0..SQUARE_WIDTH {
            if board[box_col + c][box_row + r] == num {
                return false;
            }
        }
    }

    return true;
}


fn check_safe(board: [[u32; BOARD_SIZE]; BOARD_SIZE], col: usize, row: usize, num: u32) -> bool {
    /*
    Traditional board check, will return false if parameter num is present in a col, row or box
     */
    if !check_col(board,col,num) { return false; }
    if !check_row(board,row,num) { return false; }
    return check_box(board, col, row, num);
}


fn check_safe_vec(board: [[u32; BOARD_SIZE]; BOARD_SIZE], col: usize, row: usize) -> Vec<u32> {
    /*
    Function to generate list of safe numbers in the board given a valid coordinate

    If you can let me know what data structure is appropriate here, as a vec might not be the best suit
    Same goes for population of those data structures, i think my current system is very slow
     */
    let all_numbers: Vec<_> = (1..=9).collect();

    let used_numbers = [
        check_row_vec(board, row),
        check_col_vec(board, col),
        check_box_vec(board, col, row)
    ].concat();

    // Get vector of possible numbers from all numbers filtering out numbers that are present in the used numbers
    let possible_numbers: Vec<u32> = all_numbers
        .iter()
        .copied()
        .filter(|n| !used_numbers.contains(&n))
        .collect::<Vec<u32>>();

    return possible_numbers;
}


fn vec_solve(board: &mut [[u32; BOARD_SIZE]; BOARD_SIZE], mut col: usize, mut row: usize) -> bool {
    /*
    Recursive backtracking algorithm to solve board, has vector generation which slows down alg
     */

    // Dealing with coordinate input
    if col < BOARD_SIZE - 1 && row == BOARD_SIZE {
        col += 1; row = 0;
    }
    // If the end of the board has been reached we know the algorithm is done and the process can end
    else if row == BOARD_SIZE { return true; }

    // If the current coordinate is non zero we can move ahead one place with a recursion
    if board[col][row] > 0 {
        return vec_solve(board,col,row + 1);
    }

    // Generate data structure of safe numbers that can be used\
    // I BELIEVE THIS IS WHERE A LOT OF TIME IS LOST
    let safe_numbers: Vec<u32> = check_safe_vec(*board, col, row);
    for num in safe_numbers {
        board[col][row] = num;
        if vec_solve(board, col, row + 1) { return true; }
    }

    // If the choice in number couldn't produce a full board we reset the board up to the point and try again
    board[col][row] = 0;

    return false;
}


fn solve(board: &mut [[u32; BOARD_SIZE]; BOARD_SIZE], mut col: usize, mut row: usize) -> bool {
    /*
    More traditional recursive backtracking algorithm, works identically to vec_solve but instead checks
    all numbers from 1-9, faster
     */

    if col < BOARD_SIZE - 1 && row == BOARD_SIZE {
        col += 1; row = 0;
    } else if row == BOARD_SIZE { return true; }

    if board[col][row] > 0 {
        return solve(board, col, row + 1);
    }

    for num in 1..=9 {
        if check_safe(*board, col, row, num) {
            board[col][row] = num;
            if solve(board, col, row + 1) { return true; }
        }
        board[col][row] = 0;
    }

    return false;
}





fn display_board(board: [[u32; BOARD_SIZE]; BOARD_SIZE]) {
    /*
    Function to display board
     */
    for c in board {
        for r in c {
            print!("{} ",r);
        }
        print!("\n");
    }
}


fn timed_solve(mut board: [[u32; BOARD_SIZE]; BOARD_SIZE]) -> Duration {
    /*
    Function to show board states before and after solving and return the time taken to solve
     */

    display_board(board);

    let now = Instant::now();
    solve(&mut board, 0, 0);
    let end = now.elapsed();

    print!("\n");
    display_board(board);
    println!("{:?}", end);

    return end;
}


fn open_file<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
    where P: AsRef<Path>, {
        /*
        Function to open file and get lines from file
         */
        let file = File::open(filename)?;
        Ok(io::BufReader::new(file).lines())
}


fn read_and_solve(board: &mut [[u32; BOARD_SIZE]; BOARD_SIZE]) {
    /*
    Function to solve set of 1000 boards and time each solve
     */
    let mut time_vec: Vec<Duration> = vec![];

    if let Ok(lines) = open_file("./src/sudoku_puzzles.txt") {
        let mut c: usize = 0;
        let mut r: usize = 0;

        for line in lines.flatten() {

            if c < 8 && r == 9 {
                c += 1; r = 0;
            }

            if line.eq("-") {
                // When a "-" is found the board read has ended and the board can be solved in its current state
                c = 0;
                r = 0;
                let time: Duration = timed_solve(*board);
                time_vec.push(time);
            } else {
                // Add numbers from line read to board
                for lr in line.chars() {
                    board[c][r] = lr.to_digit(10).unwrap();
                    r += 1;
                }
            }
        }
    }
}


fn main() {
    let mut board: [[u32; BOARD_SIZE]; BOARD_SIZE] = [
                                    [5,3,0,0,7,0,0,0,0],
                                    [6,0,0,1,9,5,0,0,0],
                                    [0,9,8,0,0,0,0,6,0],
                                    [8,0,0,0,6,0,0,0,3],
                                    [4,0,0,8,0,3,0,0,1],
                                    [7,0,0,0,2,0,0,0,6],
                                    [0,6,0,0,0,0,2,8,0],
                                    [0,0,0,4,1,9,0,0,5],
                                    [0,0,0,0,8,0,0,7,9]
    ];
    read_and_solve(&mut board);

    print!("\n");

}