# Unit 3: Testing and Code Quality with Jest
## Practical Assignment

### Setup Instructions
1. Make sure Node.js is installed on your computer
2. Create a new directory for your project
3. Initialize a new Node.js project using `npm init -y`
4. Install Jest using `npm install --save-dev jest`
5. Update package.json to add Jest as the test runner:
   ```json
   {
     "scripts": {
       "test": "jest"
     }
   }
   ```

### Task
You will be working with a simple calculator module and writing tests for it using Jest. Create two files:
- `calculator.js`: Contains the calculator functions
- `calculator.test.js`: Contains the test cases

### Questions and Tasks

1. Create a basic calculator module with an `add` function that adds two numbers.
   - Write a test case to verify that 2 + 3 equals 5
   - Write a test case to verify that (-2) + (-3) equals -5

**Answer 1:**
```javascript
// calculator.js
function add(a, b) {
    return a + b;
}
module.exports = { add };

// calculator.test.js
const { add } = require('./calculator');

test('adds 2 + 3 to equal 5', () => {
    expect(add(2, 3)).toBe(5);
});

test('adds (-2) + (-3) to equal -5', () => {
    expect(add(-2, -3)).toBe(-5);
});
```

2. Add a `multiply` function to your calculator module.
   - Write a test case to verify that 4 × 5 equals 20
   - Write a test case to verify that 0 × 100 equals 0

**Answer 2:**
```javascript
// calculator.js
function multiply(a, b) {
    return a * b;
}
module.exports = { add, multiply };

// calculator.test.js
test('multiplies 4 × 5 to equal 20', () => {
    expect(multiply(4, 5)).toBe(20);
});

test('multiplies 0 × 100 to equal 0', () => {
    expect(multiply(0, 100)).toBe(0);
});
```

3. Create a test suite (describe block) for testing multiple related operations.
   - Group your addition tests together
   - Group your multiplication tests together

**Answer 3:**
```javascript
// calculator.test.js
describe('Calculator Addition', () => {
    test('adds 2 + 3 to equal 5', () => {
        expect(add(2, 3)).toBe(5);
    });
    
    test('adds (-2) + (-3) to equal -5', () => {
        expect(add(-2, -3)).toBe(-5);
    });
});

describe('Calculator Multiplication', () => {
    test('multiplies 4 × 5 to equal 20', () => {
        expect(multiply(4, 5)).toBe(20);
    });
    
    test('multiplies 0 × 100 to equal 0', () => {
        expect(multiply(0, 100)).toBe(0);
    });
});
```

4. Add input validation to your calculator functions and write tests for invalid inputs.
   - Test that passing strings throws an error
   - Test that passing undefined throws an error

**Answer 4:**
```javascript
// calculator.js
function validateNumbers(a, b) {
    if (typeof a !== 'number' || typeof b !== 'number') {
        throw new Error('Inputs must be numbers');
    }
}

function add(a, b) {
    validateNumbers(a, b);
    return a + b;
}

// calculator.test.js
test('throws error when adding strings', () => {
    expect(() => add('2', '3')).toThrow('Inputs must be numbers');
});

test('throws error when adding undefined values', () => {
    expect(() => add(undefined, 5)).toThrow('Inputs must be numbers');
});
```

5. Write a test that uses Jest's `beforeEach` to set up common test values.
   - Create test variables that will be reset before each test
   - Write two tests that use these variables

**Answer 5:**
```javascript
let num1, num2;

beforeEach(() => {
    num1 = 10;
    num2 = 5;
});

test('common variables addition', () => {
    expect(add(num1, num2)).toBe(15);
});

test('common variables multiplication', () => {
    expect(multiply(num1, num2)).toBe(50);
});
```

6. Create a function that returns an array of calculation results and test it using `toEqual`.
   - The function should perform multiple calculations
   - Test the entire array output

**Answer 6:**
```javascript
// calculator.js
function calculateMany(a, b) {
    return [
        add(a, b),
        multiply(a, b)
    ];
}

// calculator.test.js
test('performs multiple calculations', () => {
    expect(calculateMany(3, 4)).toEqual([7, 12]);
});
```

7. Write tests using Jest matchers other than `.toBe()`.
   - Use `.toBeGreaterThan()`
   - Use `.toBeLessThan()`
   - Use `.toBeCloseTo()` for decimal calculations

**Answer 7:**
```javascript
test('using different Jest matchers', () => {
    expect(add(5, 5)).toBeGreaterThan(8);
    expect(multiply(2, 3)).toBeLessThan(7);
    expect(add(0.1, 0.2)).toBeCloseTo(0.3);
});
```

8. Create a function that returns an object with calculation results and test it.
   - The object should contain multiple calculation results
   - Test the object structure using `.toHaveProperty()`

**Answer 8:**
```javascript
// calculator.js
function calculateResults(a, b) {
    return {
        sum: add(a, b),
        product: multiply(a, b)
    };
}

// calculator.test.js
test('calculation results object', () => {
    const results = calculateResults(3, 4);
    expect(results).toHaveProperty('sum', 7);
    expect(results).toHaveProperty('product', 12);
});
```

9. Write a test that checks for floating-point precision issues.
   - Test addition of decimal numbers
   - Use `.toBeCloseTo()` instead of `.toBe()`

**Answer 9:**
```javascript
test('handles floating point precision', () => {
    expect(add(0.1, 0.2)).toBeCloseTo(0.3);
    expect(add(0.01, 0.02)).toBeCloseTo(0.03);
});
```

10. Create a test that uses Jest's `test.each` to run the same test with different inputs.
    - Test addition with multiple pairs of numbers
    - Include both positive and negative numbers

**Answer 10:**
```javascript
test.each([
    [1, 1, 2],
    [2, 3, 5],
    [-1, 1, 0],
    [-2, -2, -4]
])('adds %i + %i to equal %i', (a, b, expected) => {
    expect(add(a, b)).toBe(expected);
});
```

### Submission Instructions
1. Ensure all your code is saved in the required files
2. Run all tests using `npm test` and verify they pass
3. Submit both your `calculator.js` and `calculator.test.js` files
4. Include a screenshot of your passing test results

### Grading Criteria
- All tests pass successfully (40%)
- Proper use of Jest testing features (30%)
- Code quality and organization (20%)
- Proper error handling and validation (10%)
