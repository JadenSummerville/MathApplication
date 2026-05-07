package temp_code;


import java.util.Random;

public class Number
{
    private static final Random RANDOM = new Random();
    private static final int[] primes = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97};
    private final int[] powers = new int[primes.length];
    private long remainder;
    private boolean isPositive;
    public Number(long num)
    {
        if(num == 0)
        {
            for(int i = 0; i != powers.length; i++)
            {
                
            }
            isPositive = RANDOM.nextBoolean();
            remainder = 0;
            return;
        }
        if(num < 0)
        {
            num *= -1;
            isPositive = false;
        }
        else
        {
            isPositive = true;
        }
    }
    public static void main(String[] args) {
    }
    private long convertToValue()
    {
        long num;
        if(isPositive)
        {
            num = 1;
        }
        else
        {
            num = -1;
        }
        for(int i = 0; i != primes.length; i++)
        {
            num *= Math.pow(primes[i], powers[i]);
        }
        return num * remainder;
    }
}