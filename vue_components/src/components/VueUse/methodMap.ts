import { initBreakpoints } from "./useBreakpoints";
import { initUseDark } from "./useDark";
import { initUseQRCode } from "./useQRCode";

export class MethodInfo {
  private methods = new Map<string, Function>();

  constructor() {}

  public addMethod(name: string, method: Function) {
    this.methods.set(name, method);
  }

  public getAllMethods() {
    return Object.fromEntries(this.methods.entries());
  }
}

const methodMap = new Map<string, Function>([
  ["useBreakpoints", initBreakpoints],
  ["useDark", initUseDark],
  ["useQRCode", initUseQRCode],
]);

export function getMethod(
  name: string,
  methodArgs: any[] = [],
  emit: Function
): MethodInfo {
  if (!methodMap.has(name)) {
    throw new Error(`Method ${name} not found`);
  }

  return methodMap.get(name)!(...methodArgs, emit);
}
