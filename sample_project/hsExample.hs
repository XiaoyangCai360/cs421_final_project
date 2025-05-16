-- HsExample.hs
-- TODO: write module header documentation

module HsExample where

-- TODO: implement fibonacci (naïve recursion)
fibonacci :: Int -> Int
fibonacci 0 = 0
fibonacci 1 = 1
fibonacci n = fibonacci (n - 1) + fibonacci (n - 2)

-- FIXME: add memoization for performance
