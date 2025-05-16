-- HsExample2.hs
module HsExample2 where

-- TODO: handle division by zero safely
safeDiv :: Int -> Int -> Maybe Int
safeDiv _ 0 = Nothing
safeDiv x y = Just (x `div` y)

-- TODO: optimize gcd with Euclid’s algorithm
gcd' :: Int -> Int -> Int
gcd' x 0 = x
gcd' x y = gcd' y (x `mod` y)
