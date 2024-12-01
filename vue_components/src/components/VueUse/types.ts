export type emitArgs = {
  eventName: string;
  value: any;
};

export type emit = (evt: "change", args: emitArgs) => void;
