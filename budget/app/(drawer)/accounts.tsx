import { Stack } from 'expo-router';
import * as React from 'react';
import { View, Pressable, TextInput } from 'react-native';
import { Icon } from '@roninoss/icons';
import { FlashList } from '@shopify/flash-list';

import { Container } from '~/components/Container';
import { Text } from '~/components/nativewindui/Text';
import { Toggle } from '~/components/nativewindui/Toggle';
import { useColorScheme } from '~/lib/useColorScheme';

// Mock data structure for accounts
type AccountTransaction = {
  id: string;
  selected?: boolean;
  account: string;
  date: string;
  payee: string;
  category: string;
  memo: string;
  outflow?: number;
  inflow?: number;
  cleared: boolean;
};

// Mock data
const mockTransactions: AccountTransaction[] = [
  {
    id: '1',
    account: 'Itau Cartão',
    date: '18/02/2025',
    payee: 'Manual Balance Adjustment',
    category: 'Inflow: Ready to Assign',
    memo: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
    inflow: 14539.58,
    cleared: true,
  },
  {
    id: '2',
    account: 'Itau Cartão',
    date: '18/02/2025',
    payee: 'Manual Balance Adjustment',
    category: 'Inflow: Ready to Assign',
    memo: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
    outflow: 14539.58,
    cleared: false,
  },
  {
    id: '3',
    account: 'Itau Cartão',
    date: '18/02/2025',
    payee: 'Manual Balance Adjustment',
    category: 'Inflow: Ready to Assign',
    memo: '',
    outflow: 14539.58,
    cleared: false,
  },
];

const TableHeader = () => (
  <View className="grid grid-cols-9 items-center border-b border-border bg-card px-2 py-3">
    <View className="w-4" />
    <Text className="w-24 font-medium truncate">Account</Text>
    <Text className="w-20 font-medium truncate">Date</Text>
    <Text className="w-32 font-medium truncate">Payee</Text>
    <Text className="flex-1 font-medium truncate">Category</Text>
    <Text className="w-32 font-medium truncate">Memo</Text>
    <Text className="w-24 font-medium text-right">Outflow</Text>
    <Text className="w-24 font-medium text-right">Inflow</Text>
    <View className="w-4" />
  </View>
);

type TableRowProps = {
  item: AccountTransaction;
  onToggleSelect: (id: string) => void;
  onToggleCleared: (id: string) => void;
  onUpdateMemo: (id: string, memo: string) => void;
};

const TableRow = React.memo(({ item, onToggleSelect, onToggleCleared, onUpdateMemo }: TableRowProps) => {
  const { colors } = useColorScheme();
  const [isEditingMemo, setIsEditingMemo] = React.useState(false);
  const [memoText, setMemoText] = React.useState(item.memo);
  
  const handleMemoSubmit = () => {
    onUpdateMemo(item.id, memoText);
    setIsEditingMemo(false);
  };

  return (
    <View className="grid grid-cols-9 items-center border-b border-border bg-white dark:bg-transparent px-2 py-3">
      <View className="w-4 items-center justify-center">
        <Toggle
          value={item.selected}
          onValueChange={() => {
            onToggleSelect(item.id);
          }}
        />
      </View>
      <Text className="w-24 truncate" color="secondary">{item.account}</Text>
      <Text className="w-20" color="secondary">{item.date}</Text>
      <Text className="w-32 truncate" color="secondary">{item.payee}</Text>
      <Text className="flex-1 truncate" color="secondary">{item.category}</Text>
      <Pressable className="w-32 min-h-[24px]" onPress={() => setIsEditingMemo(true)}>
        {isEditingMemo ? (
          <TextInput
            value={memoText}
            onChangeText={setMemoText}
            onBlur={handleMemoSubmit}
            onSubmitEditing={handleMemoSubmit}
            autoFocus
            placeholder="Add memo"
            placeholderTextColor={colors.grey2}
            className="border border-border rounded px-2 py-1 dark:text-white w-full h-full"
          />
        ) : (
          <Text color="secondary" className="truncate min-h-[24px]">
            {item.memo || " "}
          </Text>
        )}
      </Pressable>
      <Text className="w-24 text-right" color="secondary">
        {item.outflow ? `R$${item.outflow.toFixed(2)}` : ''}
      </Text>
      <Text className="w-24 text-right" color="primary">
        {item.inflow ? `R$${item.inflow.toFixed(2)}` : ''}
      </Text>
      <View className="w-4 items-center justify-center">
        <Toggle
          value={item.cleared}
          onValueChange={() => {
            onToggleCleared(item.id);
          }}
        />
      </View>
    </View>
  );
});

TableRow.displayName = 'TableRow';

export default function Accounts() {
  const [transactions, setTransactions] = React.useState(mockTransactions);

  const toggleSelection = React.useCallback((id: string) => {
    setTransactions(prev =>
      prev.map(t =>
        t.id === id ? { ...t, selected: !t.selected } : t
      )
    );
  }, []);

  const toggleCleared = React.useCallback((id: string) => {
    setTransactions(prev =>
      prev.map(t =>
        t.id === id ? { ...t, cleared: !t.cleared } : t
      )
    );
  }, []);

  const updateMemo = React.useCallback((id: string, memo: string) => {
    setTransactions(prev =>
      prev.map(t =>
        t.id === id ? { ...t, memo } : t
      )
    );
  }, []);

  return (
    <>
      <Stack.Screen options={{ title: 'Accounts' }} />
      <Container>
        <View className="flex-1 border border-border rounded-lg overflow-hidden">
          <TableHeader />
          <FlashList
            data={transactions}
            renderItem={({ item }) => (
              <TableRow 
                item={item} 
                onToggleSelect={toggleSelection}
                onToggleCleared={toggleCleared}
                onUpdateMemo={updateMemo}
              />
            )}
            estimatedItemSize={56}
            keyExtractor={item => item.id}
          />
        </View>
      </Container>
    </>
  );
} 