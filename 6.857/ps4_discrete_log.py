import time
import math

class ProblemStatement:
  def __init__(self, i, r, s, p, g, h):
    self.i = i
    self.r = r
    self.s = s
    self.p = p
    self.g = g
    self.h = h

class QuadraticDiscreteLog:
  def __init__(self, problem_statement):
    self.problem_statement = problem_statement
    self.prime = problem_statement.p

  def solve_problem(self, z):
    z_to_s = self.repeated_squaring(z, self.problem_statement.s, self.prime)
    z_to_r = self.repeated_squaring(z, self.problem_statement.r, self.prime)
    a = self.naive_discrete_logarithm(self.problem_statement.g, z_to_s, self.problem_statement.r)
    b = self.naive_discrete_logarithm(self.problem_statement.h, z_to_r, self.problem_statement.s)

    a = self.modular_inverse(self.problem_statement.s, self.problem_statement.r)*a % self.problem_statement.r
    b = self.modular_inverse(self.problem_statement.r, self.problem_statement.s)*b % self.problem_statement.s

    return (a, b)

  def naive_solve_problem(self, z):
    result_cache = {}
    g = self.problem_statement.g
    h = self.problem_statement.h

    g_to_a = 1
    for a in xrange(self.problem_statement.r):
      mga = self.find_offset_inverse(g_to_a, z)
      result_cache[mga] = a
      g_to_a = (g_to_a * g) % self.prime

    h_to_b = 1
    for b in xrange(self.problem_statement.s):
      if h_to_b in result_cache:
        return (result_cache[h_to_b], b)

      h_to_b = (h_to_b * h) % self.prime
    raise Exception("No Results Found")

  def check_result(self, result_a, result_b, z):
    ga_mod_p = self.repeated_squaring(self.problem_statement.g, result_a, self.prime)
    hb_mod_p = self.repeated_squaring(self.problem_statement.h, result_b, self.prime)

    return (ga_mod_p * hb_mod_p % self.prime) == (z % self.prime)

  # Solves the equation for m:
  #   m * value = z mod p
  # This method solves the above by finding the inverse of value and multiplying
  # it with z to obtain m.
  def find_offset_inverse(self, value, z):
    return (self.find_inverse(value)*z) % self.prime

  ########################
  #### Helper methods ####
  ########################

  def naive_discrete_logarithm(self, generator, element, order):
    current_power = 1
    element %= self.prime
    for j in xrange(order):
      if element == current_power:
        return j
      current_power = (current_power * generator) % self.prime

  def discrete_logarithm(self, generator, element, order):
    max_iteration = int(math.ceil(math.sqrt(order)))
    current_power = 1
    result_cache = {}
    for j in xrange(max_iteration):
      result_cache[current_power] = j
      current_power = (generator * current_power) % self.prime

    inverse = self.find_inverse(generator)
    inverse_gen = self.repeated_squaring(inverse, max_iteration, self.prime)
    current_result = element
    for i in xrange(max_iteration):
      if current_result in result_cache:
        return i*m + result_cache[current_result]

      current_result = (current_result * inverse_gen) % self.prime

  def repeated_squaring(self, base, exponent, modulo):
    value = base
    current_exponent = 1
    while current_exponent*2 <= exponent:
      current_exponent *= 2
      value = value**2 % modulo

    # finish off the calculation
    for i in xrange(current_exponent, exponent):
      value = value*base % modulo

    return value

  def find_inverse(self, value):
    return self.modular_inverse(value, self.prime)

  def modular_inverse(self, a, p):
    x, y = self.extended_gcd(a, p)
    return x % p

  def extended_gcd(self, a, b):
    x = 0
    y = 1
    last_x = 1
    last_y = 0
    while b != 0:
      quotient = a / b
      a, b = b, a % b
      x, last_x = last_x - quotient*x, x
      y, last_y = last_y - quotient*y, y
    return (last_x, last_y)

if __name__ == '__main__':
  #  'john': 146689,
  #  'hrishi': 22801,
  #  'mari': 58081
  #  'chidubem': 4489
  z = 146689 * 22801 * 58081 * 4489

  problems = [
    #ProblemStatement(40,524309,524731,550242371759,519522491680,503576381150),
    #ProblemStatement(48,8388619,8389301,140749299530639,66037182322460,135464719185218),
    #ProblemStatement(56,134217757,134217827,36028831378708079,16299632003719340,16774991081098723),
    #ProblemStatement(64,2147483693,2147483713,9223372509301184219,3696004885659783518,7370438810086932486),
    #ProblemStatement(72,34359738421,34359738839,2361183277443828466439,1200900809020609343714,1434335674966405528239),
    ProblemStatement(80,549755813911,549755814143,604462910112978819886547,183883715113935111825201,100918460208293533427177),
    #ProblemStatement(88,8796093022247,8796093022513,154742504916724246361693423,119979762901203886458785425,19944507889608836377996103),
    #ProblemStatement(96,140737488355369,140737488355601,39614081257220551939459143539,4139919584394033405273246004,5499605979443036648738685765),
    #ProblemStatement(104,2251799813685313,2251799813685641,10141204801827897860602961381267,7433470851204605199455053815761,2285408186981182964649900757827),
    #ProblemStatement(112,36028797018963971,36028797018964051,2596148429267420011218335426413043,2415361387207098342427240835373288,1375659042404400759015490195766754),
    #ProblemStatement(120,576460752303423649,576460752303423737,664613997892458409149720418947512627,38587807275483205975177192303754311,551313375005300229885194641826801267),
    #ProblemStatement(128,9223372036854776167,9223372036854777059,170141183460469261430945262388263105707,63195444409474387481625570646916067327,85806326020200823913514852048625758577),
    #ProblemStatement(136,147573952589676413083,147573952589676413147,43556142965880123433697266288344288004403,13919914095470414314154361939495832819948,18859771708954736140181014691666795631453),
    #ProblemStatement(144,2361183241434822606859,2361183241434822607637,11150372599265311574545752322619896923964367,3517547304865782888300641560670957747688839,9585772641946202726839066002560811221527552),
    #ProblemStatement(152,37778931862957161709829,37778931862957161710161,2854495385411919762181098354520921104965744939,2258654064183684636977530559218688554603251068,1492700112058499579984198687124924995940137115),
    #ProblemStatement(160,604462909807314587353111,604462909807314587353439,730750818665451459102294554614677381139306397459,79115375331432283992754115983649531958532471430,269339689197503183029815113356998028988359849979),
    #ProblemStatement(168,9671406556917033397651183,9671406556917033397651271,187072209578355573530142027741792354850960669207187,185616401717165416874950910999255099051549606505729,86111405601092609144272675033815814454636927504114),
    #ProblemStatement(176,154742504910672534362390771,154742504910672534362390899,47890485652059026823698534622243192293957794583986259,42892134034408674442506017463415437827554967128152799,12529640564565304854530723937246428646631003185413626),
    #ProblemStatement(184,2475880078570760549798248909,2475880078570760549798249669,12259964326927110866866784546063057780988402498777722243,567994488488621838322157989141724098265787217702086238,4045655895244381412194748020217674066493324505208991236),
    #ProblemStatement(192,39614081257132168796771975177,39614081257132168796771976037,3138550867693340381917894781166159895575266129363605667099,1132286656325811111857034719145211051632839313718028267962,1937341394178207224071912232024689095105214876377016223046),
    #ProblemStatement(200,633825300114114700748351603341,633825300114114700748351603609,803469022129495137770981048165863346020334574847207264115339,241096872223455165843158841196213032014274036790717505939655,760752685535450761510397371378348285529939788963742251911691),
  ]

  for ps in problems:
    start = time.time()
    discrete_log = QuadraticDiscreteLog(ps)
    a, b = discrete_log.solve_problem(z)
    end = time.time()

    print "Time: ", end - start
    print "a,b = ", a,b
