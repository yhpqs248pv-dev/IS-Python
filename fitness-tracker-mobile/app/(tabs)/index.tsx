import { useEffect, useState } from "react";
import { Text, TextInput, View, Button, ScrollView } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";

const KEY = "workouts_v1";

type LogEntry = {
  id: number;
  date: string;
  exercise: string;
  sets: string;
  reps: string;
};

export default function TabOneScreen() {
  const [exercise, setExercise] = useState("");
  const [sets, setSets] = useState("");
  const [reps, setReps] = useState("");
  const [logs, setLogs] = useState<LogEntry[]>([]);

  // load saved logs on app start
  useEffect(() => {
    (async () => {
      const raw = await AsyncStorage.getItem(KEY);
      if (raw) setLogs(JSON.parse(raw));
    })();
  }, []);

  const saveLogs = async (nextLogs: LogEntry[]) => {
    setLogs(nextLogs);
    await AsyncStorage.setItem(KEY, JSON.stringify(nextLogs));
  };

  const addLog = async () => {
    if (!exercise.trim()) return;

    const entry: LogEntry = {
      id: Date.now(),
      date: new Date().toISOString().slice(0, 10),
      exercise: exercise.trim(),
      sets: sets.trim() || "0",
      reps: reps.trim() || "0",
    };

    await saveLogs([entry, ...logs]);
    setExercise("");
    setSets("");
    setReps("");
  };

  const clearAll = async () => {
    await AsyncStorage.removeItem(KEY);
    setLogs([]);
  };

  return (
    <View style={{ flex: 1, paddingTop: 60, paddingHorizontal: 16 }}>
      <Text style={{ fontSize: 24, fontWeight: "600" }}>
        Fitness Tracker v0.2
      </Text>
      <Text style={{ marginTop: 6, marginBottom: 16 }}>
        Saved locally on this iPhone. No account. No hosting.
      </Text>

      <TextInput
        placeholder="Exercise (e.g., Bench)"
        value={exercise}
        onChangeText={setExercise}
        style={{ borderWidth: 1, padding: 12, marginBottom: 10, borderRadius: 8 }}
      />
      <TextInput
        placeholder="Sets"
        value={sets}
        onChangeText={setSets}
        keyboardType="numeric"
        style={{ borderWidth: 1, padding: 12, marginBottom: 10, borderRadius: 8 }}
      />
      <TextInput
        placeholder="Reps"
        value={reps}
        onChangeText={setReps}
        keyboardType="numeric"
        style={{ borderWidth: 1, padding: 12, marginBottom: 10, borderRadius: 8 }}
      />

      <Button title="Add log" onPress={addLog} />
      <View style={{ height: 10 }} />
      <Button title="Clear all logs" onPress={clearAll} />

      <Text style={{ marginTop: 20, fontSize: 18, fontWeight: "600" }}>
        Recent
      </Text>

      <ScrollView style={{ marginTop: 10 }}>
        {logs.length === 0 ? (
          <Text>No logs yet.</Text>
        ) : (
          logs.map((l) => (
            <View
              key={l.id}
              style={{ paddingVertical: 10, borderBottomWidth: 1 }}
            >
              <Text style={{ fontWeight: "600" }}>
                {l.date} — {l.exercise}
              </Text>
              <Text>
                {l.sets} x {l.reps}
              </Text>
            </View>
          ))
        )}
      </ScrollView>
    </View>
  );
}
