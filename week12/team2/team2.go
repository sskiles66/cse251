/* ---------------------------------------
Course: CSE 251
Lesson Week: ?12
File: team.go
Author: Brother Comeau

Purpose: team activity - finding primes

Instructions:

- Process the array of numbers, find the prime numbers using goroutines

worker()

This goroutine will take in a list/array/channel of numbers.  It will place
prime numbers on another channel

readValue()

This goroutine will display the contents of the channel containing
the prime numbers

--------------------------------------- */
package main

import (
	"fmt"
	"math/rand"
	"time"
	"sync"
)

func isPrime(n int) bool {
	// Primality test using 6k+-1 optimization.
	// From: https://en.wikipedia.org/wiki/Primality_test

	if n <= 3 {
		return n > 1
	}

	if n%2 == 0 || n%3 == 0 {
		return false
	}

	i := 5
	for (i * i) <= n {
		if n%i == 0 || n%(i+2) == 0 {
			return false
		}
		i += 6
	}
	return true
}

func worker(wg *sync.WaitGroup, numbers <-chan int, primes chan<- int) {
    defer wg.Done()
    for n := range numbers {
        if isPrime(n) {
            primes <- n
        }
    }
}

func readValues(primes <-chan int) {
    for prime := range primes {
        fmt.Println(prime)
    }
}

func main() {
    workers := 10
    numberValues := 100

    numbers := make(chan int)
    primes := make(chan int)

    var wg sync.WaitGroup
    wg.Add(workers)

    for w := 1; w <= workers; w++ {
        go worker(&wg, numbers, primes)
    }

    rand.Seed(time.Now().UnixNano())
    for i := 0; i < numberValues; i++ {
        numbers <- rand.Int()
    }
    close(numbers)

    go func() {
        wg.Wait()
        close(primes)
    }()

    readValues(primes)

    fmt.Println("All Done!")
}