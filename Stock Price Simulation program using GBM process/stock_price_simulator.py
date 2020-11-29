# Imports
from random import gauss, seed
from math import sqrt, exp

# Create a function based on GBM to execute stock price simulation
def create_GBM(s0, mu, sigma):
  """
  Generates a price following a Geometric Brownian Motion process based on the input of the arguments:
  - s0: Asset inital price.
  - mu: Interest rate expressed annual terms.
  - sigma: Volatility expressed annual terms. 
  """
  sp = s0

  # Generate stock value for the current simulation step
  def generate_value():
    nonlocal sp
    sp *= exp((mu - 0.5 * sigma ** 2) * (1.0 / 365.0) + sigma * sqrt(1.0/365.0) * gauss(mu=0, sigma=1))
    return sp
  return generate_value

if __name__ == "__main__":
  seed(1234)           # Target achieved
  # seed(2234)           # Target failed
  gbm = create_GBM(100, 0.1, 0.05)

  for _ in range(1000):
      sp = gbm()
      print(sp)
      if sp >= 130.0:
          print("Target reached, profit earned.")
          break
  else:
      print("Did not achieve target price.")
  print(sp)