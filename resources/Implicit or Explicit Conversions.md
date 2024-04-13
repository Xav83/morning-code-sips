# Implicit and Explicit conversion

| Consideration | Your Class? | Your Class? | Your Class? |
|---|---|---|---|
| same platonic thing? | yes | no[1] | - |
| info fidelity | no loss | some loss | more loss |
| performance penalty? | little/no | some | yes |
| throws? | noexcept?/rarely?/ same as copyctor? | yes | - |
| danger? (dangling, etc) | no | yes | - |
| code review? | no need | self-policed[2] | greppable / policeable |
| generic code? | strict | less strict | “extension point” |
| can modify class? | yes | yes | no |
| are you sure? | yes | no | - |
| **Result** | **Implicit ctor/cast** | **Explicit cast/ctor Named** | **Explicit cast/ctor Named** |

1. If not the same platonic thing, you can have an explicit constructor, but you shouldn’t have a cast at all
2. ‘self-policed’ - Explicit conversions are more for situations where you want the developer to stop for a second and think about the conversion, but have enough faith in the average developer to make a good choice, and don’t feel it typically needs much further policing. You can see it in a code review, but harder to grep for.


Source: [https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/p0705r0.html](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/p0705r0.html)

Document exported by Xavier Jouvenot ([@10xLearner](https://twitter.com/10xLearner))